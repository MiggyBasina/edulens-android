    import os
import json
import pickle
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

class SimpleCache:
    """Lightweight file cache for mobile performance"""
    
    def __init__(self, name="app_cache", max_size_mb=50):
        self.cache_dir = Path(name)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
        self._cleanup_if_needed()
    
    def _get_filepath(self, key):
        """Get filepath for cache key"""
        safe_key = hashlib.md5(str(key).encode()).hexdigest()
        return self.cache_dir / safe_key
    
    def _cleanup_if_needed(self):
        """Cleanup if cache is too large"""
        try:
            total_size = sum(f.stat().st_size for f in self.cache_dir.glob('*') if f.is_file())
            if total_size > self.max_size:
                # Delete oldest files
                files = [(f, f.stat().st_mtime) for f in self.cache_dir.glob('*') if f.is_file()]
                files.sort(key=lambda x: x[1])  # Sort by modification time
                
                # Delete until under 80% of max size
                target_size = self.max_size * 0.8
                for file, _ in files:
                    if total_size <= target_size:
                        break
                    try:
                        total_size -= file.stat().st_size
                        file.unlink()
                    except:
                        pass
        except:
            pass
    
    def set(self, key, data, ttl_hours=24):
        """Cache data with TTL"""
        try:
            filepath = self._get_filepath(key)
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'ttl_hours': ttl_hours,
                'data': data
            }
            with open(filepath, 'wb') as f:
                pickle.dump(cache_data, f)
            return True
        except:
            return False
    
    def get(self, key, default=None):
        """Get cached data if not expired"""
        try:
            filepath = self._get_filepath(key)
            if not filepath.exists():
                return default
            
            with open(filepath, 'rb') as f:
                cache_data = pickle.load(f)
            
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            ttl = timedelta(hours=cache_data.get('ttl_hours', 24))
            
            if datetime.now() - cache_time > ttl:
                filepath.unlink()  # Delete expired
                return default
            
            return cache_data['data']
        except:
            return default
    
    def delete(self, key):
        """Delete cached item"""
        try:
            filepath = self._get_filepath(key)
            if filepath.exists():
                filepath.unlink()
        except:
            pass
    
    def clear(self):
        """Clear all cache"""
        try:
            for file in self.cache_dir.glob('*'):
                try:
                    file.unlink()
                except:
                    pass
            return True
        except:
            return False
    
    def get_stats(self):
        """Get cache statistics"""
        try:
            files = list(self.cache_dir.glob('*'))
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            return {
                'total_files': len(files),
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'cache_dir': str(self.cache_dir.absolute())
            }
        except:
            return {}

# Global cache instance
app_cache = SimpleCache("edulens_cache")
