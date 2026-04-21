import subprocess
import sys
import re

def run_yt_dlp_test(url):
    print(f"--- Testing yt-dlp with URL: {url} ---")
    
    # Intento con runtime de JS (node) y User-Agent de Chrome
    command = [
        'yt-dlp', 
        '--js-runtimes', 'node', 
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        '--flat-playlist', 
        '-J', 
        url
    ]
    
    print(f"Running command: {' '.join(command)}")
    
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print("SUCCESS: Got JSON information!")
        else:
            print(f"ERROR (code {process.returncode}):")
            print(f"STDERR: {stderr}")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    # Probando con una URL "muy sucia" para verificar la limpieza por regex
    test_url = " ` `https://www.youtube.com/watch?v=vJfYW5YZVtc` ` "
    
    # Nueva limpieza por regex
    url_match = re.search(r'(https?://[^\s`\'"]+)', test_url)
    if url_match:
        clean_url = url_match.group(1).strip()
    else:
        clean_url = test_url.strip()

    print(f"Original URL: '{test_url}'")
    print(f"Cleaned URL: '{clean_url}'")
    
    run_yt_dlp_test(clean_url)
