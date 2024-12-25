import requests, itertools, time, random
import concurrent.futures
from datetime import datetime
from colorama import init, Fore, Style
from collections import deque

# Initialize colorama
init()

class RobiNumberChecker:
    def __init__(self, base_number="8801886", fixed_positions=None):
        self.base_number = base_number
        self.url = "https://da-api.robi.com.bd/da-nll/free-msisdn/get-msisdn-list"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.fixed_positions = fixed_positions or {}
        self.available_numbers = []
        self.checked_numbers = set()  # Keep track of successfully checked numbers
        self.retry_queue = deque()    # Queue for failed numbers
        self.max_retries = 3          # Maximum number of retries per number
        self.filename = f"available_numbers_robi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
    def generate_payload(self, number):
        return {
            "msisdn": number,
            "brand": "ROBI",
            "simCategory": "PREPAID"
        }
    
    def check_number(self, number):
        if number in self.checked_numbers:
            return True

        retries = 0
        while retries < self.max_retries:
            try:
                # Add random delay between 0.1 to 0.5 seconds to prevent rate limiting
                time.sleep(random.uniform(0.1, 0.5))
                
                response = requests.post(
                    self.url,
                    headers=self.headers,
                    json=self.generate_payload(number),
                    timeout=15  # Increased timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.checked_numbers.add(number)
                    
                    if data.get("available") is True:
                        print(f"{Fore.GREEN}Found available number: {number}{Style.RESET_ALL}")
                        self.available_numbers.append(number)
                        self.save_number(number)
                    else:
                        print(f"{Fore.RED}Number not available: {number}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.YELLOW}Error checking {number}: Status code {response.status_code}{Style.RESET_ALL}")
                    retries += 1
                    time.sleep(1)  # Wait before retry
            except Exception as e:
                print(f"{Fore.RED}Error checking {number}: {str(e)}{Style.RESET_ALL}")
                retries += 1
                time.sleep(1)  # Wait before retry
        
        # If all retries failed, add to retry queue
        if number not in self.checked_numbers:
            self.retry_queue.append(number)
        return False

    def generate_numbers(self):
        remaining_digits = 6 - len(self.fixed_positions)
        positions = sorted(self.fixed_positions.keys())
        
        for combo in itertools.product(range(10), repeat=remaining_digits):
            number = list('000000')
            
            for pos, val in self.fixed_positions.items():
                number[pos] = str(val)
            
            current_combo_index = 0
            for i in range(6):
                if i not in self.fixed_positions:
                    number[i] = str(combo[current_combo_index])
                    current_combo_index += 1
            
            yield self.base_number + ''.join(number)

    def save_number(self, number):
        with open(self.filename, 'a') as f:
            f.write(f"{number}\n")

    def process_retry_queue(self):
        print(f"\n{Fore.YELLOW}Processing retry queue... ({len(self.retry_queue)} numbers){Style.RESET_ALL}")
        while self.retry_queue:
            number = self.retry_queue.popleft()
            if number not in self.checked_numbers:
                self.check_number(number)

    def run(self, max_workers=5):  # Reduced number of workers for better stability
        print(f"{Fore.CYAN}Starting number check with {max_workers} workers...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Base number: {self.base_number}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Fixed positions: {self.fixed_positions}{Style.RESET_ALL}")
        
        # First pass: check all numbers
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.check_number, number) 
                      for number in self.generate_numbers()]
            concurrent.futures.wait(futures)
        
        # Process retry queue until empty or max attempts reached
        retry_attempts = 0
        while self.retry_queue and retry_attempts < 3:
            self.process_retry_queue()
            retry_attempts += 1
            time.sleep(2)  # Wait between retry batches
        
        print(f"\n{Fore.GREEN}Search completed!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Found {len(self.available_numbers)} available numbers{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Results saved to: {self.filename}{Style.RESET_ALL}")
        if self.retry_queue:
            print(f"{Fore.YELLOW}Warning: {len(self.retry_queue)} numbers could not be checked{Style.RESET_ALL}")

if __name__ == "__main__":
    fixed_positions = {
        # 0: 8,    # First digit of the last 6 digits
        # 1: 6,    # Second digit
        # 2: 3,    # Third digit
        # 3: 0,    # Fourth digit
        4: 0,    # Fifth digit
        5: 0     # Sixth digit
    }
    
    checker = RobiNumberChecker(fixed_positions=fixed_positions)
    checker.run(max_workers=5)  # Using fewer workers for better stability