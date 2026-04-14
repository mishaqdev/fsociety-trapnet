import requests
import threading
import time
from datetime import datetime
import random
import string

class HoneypotAttacker:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.successful_requests = 0
        self.failed_requests = 0
        self.active_threads = []
        
    def generate_random_credentials(self):
        """Generate random username and password"""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 12)))
        password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=random.randint(8, 16)))
        email = f"{username}@example.com"
        return username, email, password
    
    def send_login_request(self, request_id):
        """Send a login request to the honeypot"""
        username, _, password = self.generate_random_credentials()
        
        data = {
            'username': username,
            'password': password
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/login",
                data=data,
                timeout=5
            )
            if response.status_code in [200, 401, 403]:
                self.successful_requests += 1
                print(f"[✓] Login Request {request_id} - Status: {response.status_code} - User: {username}")
            else:
                self.failed_requests += 1
                print(f"[✗] Login Request {request_id} - Failed with status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.failed_requests += 1
            print(f"[✗] Login Request {request_id} - Error: {str(e)[:50]}")
    
    def send_signup_request(self, request_id):
        """Send a signup request to the honeypot"""
        username, email, password = self.generate_random_credentials()
        
        data = {
            'username': username,
            'email': email,
            'password': password
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/signup",
                data=data,
                timeout=5
            )
            if response.status_code in [200, 201, 400, 409]:
                self.successful_requests += 1
                print(f"[✓] Signup Request {request_id} - Status: {response.status_code} - User: {username}")
            else:
                self.failed_requests += 1
                print(f"[✗] Signup Request {request_id} - Failed with status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.failed_requests += 1
            print(f"[✗] Signup Request {request_id} - Error: {str(e)[:50]}")
    
    def attack_login(self, num_requests, concurrent_threads=10):
        """Launch attack on login endpoint"""
        print(f"\n[+] Starting LOGIN attack with {num_requests} requests...")
        print(f"[+] Using {concurrent_threads} concurrent threads\n")
        
        for i in range(num_requests):
            thread = threading.Thread(target=self.send_login_request, args=(i+1,))
            self.active_threads.append(thread)
            thread.start()
            
            # Limit concurrent threads
            if len(self.active_threads) >= concurrent_threads:
                for t in self.active_threads:
                    t.join()
                self.active_threads = []
            
            # Small delay to prevent overwhelming the system
            if (i + 1) % 50 == 0:
                time.sleep(0.5)
        
        # Wait for remaining threads
        for t in self.active_threads:
            t.join()
    
    def attack_signup(self, num_requests, concurrent_threads=10):
        """Launch attack on signup endpoint"""
        print(f"\n[+] Starting SIGNUP attack with {num_requests} requests...")
        print(f"[+] Using {concurrent_threads} concurrent threads\n")
        
        for i in range(num_requests):
            thread = threading.Thread(target=self.send_signup_request, args=(i+1,))
            self.active_threads.append(thread)
            thread.start()
            
            # Limit concurrent threads
            if len(self.active_threads) >= concurrent_threads:
                for t in self.active_threads:
                    t.join()
                self.active_threads = []
            
            # Small delay to prevent overwhelming the system
            if (i + 1) % 50 == 0:
                time.sleep(0.5)
        
        # Wait for remaining threads
        for t in self.active_threads:
            t.join()
    
    def attack_both(self, num_requests, concurrent_threads=10):
        """Launch attack on both login and signup endpoints alternately"""
        print(f"\n[+] Starting COMBINED attack with {num_requests} total requests...")
        print(f"[+] Alternating between login and signup endpoints\n")
        
        for i in range(num_requests):
            if i % 2 == 0:
                thread = threading.Thread(target=self.send_login_request, args=(i+1,))
            else:
                thread = threading.Thread(target=self.send_signup_request, args=(i+1,))
            
            self.active_threads.append(thread)
            thread.start()
            
            # Limit concurrent threads
            if len(self.active_threads) >= concurrent_threads:
                for t in self.active_threads:
                    t.join()
                self.active_threads = []
            
            # Small delay
            if (i + 1) % 50 == 0:
                time.sleep(0.5)
        
        # Wait for remaining threads
        for t in self.active_threads:
            t.join()
    
    def show_results(self):
        """Display attack results"""
        print("\n" + "="*50)
        print("ATTACK RESULTS")
        print("="*50)
        print(f"✓ Successful requests: {self.successful_requests}")
        print(f"✗ Failed requests: {self.failed_requests}")
        print(f"📊 Total requests: {self.successful_requests + self.failed_requests}")
        print("="*50)

def main():
    print("="*60)
    print("HONEYPOT ATTACK SIMULATOR - LAB TESTING TOOL")
    print("="*60)
    print("⚠️  WARNING: This tool is for educational purposes only!")
    print("⚠️  Use only on your own honeypot or authorized systems!\n")
    
    attacker = HoneypotAttacker()
    
    while True:
        print("\n📋 MAIN MENU")
        print("-" * 30)
        print("1. Attack LOGIN endpoint only")
        print("2. Attack SIGNUP endpoint only")
        print("3. Attack BOTH endpoints (alternating)")
        print("4. Exit")
        print("-" * 30)
        
        try:
            choice = input("\n👉 Select attack type (1-4): ").strip()
            
            if choice == '4':
                print("\n[+] Exiting attack simulator...")
                break
            
            if choice not in ['1', '2', '3']:
                print("[!] Invalid choice! Please select 1, 2, 3, or 4")
                continue
            
            # Get number of requests
            try:
                num_requests = int(input("🔢 Enter number of requests to send: ").strip())
                if num_requests <= 0:
                    print("[!] Please enter a positive number!")
                    continue
            except ValueError:
                print("[!] Please enter a valid number!")
                continue
            
            # Optional: Set concurrent threads
            try:
                concurrent = input("⚡ Enter concurrent threads (default 10, press Enter for default): ").strip()
                concurrent_threads = int(concurrent) if concurrent else 10
                if concurrent_threads <= 0:
                    concurrent_threads = 10
            except ValueError:
                concurrent_threads = 10
            
            # Execute attack
            start_time = time.time()
            
            if choice == '1':
                attacker.attack_login(num_requests, concurrent_threads)
            elif choice == '2':
                attacker.attack_signup(num_requests, concurrent_threads)
            elif choice == '3':
                attacker.attack_both(num_requests, concurrent_threads)
            
            # Show results
            elapsed_time = time.time() - start_time
            attacker.show_results()
            print(f"⏱️  Time taken: {elapsed_time:.2f} seconds")
            print(f"📈 Average requests/second: {num_requests/elapsed_time:.2f}")
            
            # Reset counters for next attack
            attacker.successful_requests = 0
            attacker.failed_requests = 0
            
            input("\n[Press Enter to continue...]")
            
        except KeyboardInterrupt:
            print("\n\n[!] Attack interrupted by user!")
            attacker.show_results()
            break
        except Exception as e:
            print(f"\n[!] An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()
