"""
Simple caching system for improved performance
"""
import json
import hashlib
from datetime import datetime, timedelta
import os
import pickle

class AnalysisCache:
    def __init__(self, ttl_minutes=60, cache_dir="cache"):
        self.ttl = timedelta(minutes=ttl_minutes)
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.memory_cache = {}
        
    def _get_key(self, user_data):
        """Generate cache key from user data"""
        # Create a deterministic key from the data
        data_str = json.dumps(user_data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get(self, user_data):
        """Get cached analysis if available"""
        key = self._get_key(user_data)
        
        # Check memory cache first
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if datetime.now() - entry['timestamp'] < self.ttl:
                print("📦 Cache hit (memory)")
                return entry['result']
        
        # Check disk cache
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    entry = pickle.load(f)
                    if datetime.now() - entry['timestamp'] < self.ttl:
                        print("📦 Cache hit (disk)")
                        # Load into memory cache
                        self.memory_cache[key] = entry
                        return entry['result']
            except:
                pass
        
        print("📦 Cache miss")
        return None
    
    def set(self, user_data, result):
        """Cache analysis result"""
        key = self._get_key(user_data)
        entry = {
            'result': result,
            'timestamp': datetime.now(),
            'user_data_summary': {
                'app_switches': user_data.get('app_switches'),
                'duration_minutes': user_data.get('duration_minutes')
            }
        }
        
        # Save to memory
        self.memory_cache[key] = entry
        
        # Save to disk
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(entry, f)
        except Exception as e:
            print(f"Cache save error: {e}")
    
    def clear_expired(self):
        """Remove expired entries"""
        now = datetime.now()
        
        # Clear from memory
        expired_keys = [
            key for key, entry in self.memory_cache.items()
            if now - entry['timestamp'] >= self.ttl
        ]
        for key in expired_keys:
            del self.memory_cache[key]
        
        # Clear from disk
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.pkl'):
                filepath = os.path.join(self.cache_dir, filename)
                try:
                    with open(filepath, 'rb') as f:
                        entry = pickle.load(f)
                        if now - entry['timestamp'] >= self.ttl:
                            os.remove(filepath)
                except:
                    # Remove corrupted cache files
                    os.remove(filepath)
    
    def get_stats(self):
        """Get cache statistics"""
        disk_files = len([f for f in os.listdir(self.cache_dir) if f.endswith('.pkl')])
        return {
            "memory_entries": len(self.memory_cache),
            "disk_entries": disk_files,
            "cache_dir": self.cache_dir,
            "ttl_minutes": self.ttl.total_seconds() / 60
        }