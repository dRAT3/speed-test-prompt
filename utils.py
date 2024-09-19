import asyncio
import time

class TokenBucket:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TokenBucket, cls).__new__(cls)
        return cls._instance

    def __init__(self, capacity=10, refill_rate=0.5):
        if not hasattr(self, 'initialized'):
            self.capacity = capacity  # Maximum tokens in the bucket
            self.refill_rate = refill_rate  # Tokens added per second
            self.current_tokens = capacity  # Current tokens
            self.last_refill_time = time.time()  # Last time tokens were refilled
            self.initialized = True
            asyncio.create_task(self.start_refill())  # Start the refill task

    async def refill(self):
        """Refills the bucket based on the time elapsed."""
        now = time.time()
        elapsed = now - self.last_refill_time

        # Calculate the number of tokens to add
        tokens_to_add = elapsed * self.refill_rate

        # Update the current_tokens and last_refill_time
        if tokens_to_add > 0:
            self.current_tokens = min(self.capacity, self.current_tokens + tokens_to_add)
            self.last_refill_time = now

    async def start_refill(self):
        """Starts a loop to refill the bucket periodically."""
        while True:
            await asyncio.sleep(1)  # Wait for 1 second between refills
            await self.refill()  # Refill tokens periodically

    async def get_tokens(self, tokens_needed):
        """Try to get tokens from the bucket."""
        await self.refill()  # Refill bucket before attempting to get tokens

        if tokens_needed <= self.current_tokens:
            self.current_tokens -= tokens_needed  # Remove tokens
            return True  # Allowed to send
        else:
            return False  # Not allowed to send

# Global singleton instance of the TokenBucket
bucket_instance = TokenBucket(capacity=10, refill_rate=5)
