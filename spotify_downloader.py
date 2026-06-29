import subprocess
import sys
import os
import shutil

# --- Configuration ---
# Add your Spotify playlist, album, track, or liked songs URLs here.
# Example: SPOTIFY_URLS = ["https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"]
SPOTIFY_URLS = [
    # "INSERT_YOUR_URL_HERE",
    "https://open.spotify.com/playlist/70Ug9FlqMvTFCa7mq3R8dT?si=604d8dfcf6764ca1",
    "https://open.spotify.com/playlist/61EDJvC5ACCxlT9cTRXQ0l?si=69b68d9f9ed74332",
    "https://open.spotify.com/playlist/2dR00JPa2X493BOk9rDTaz?si=a826aec9f40c45a5",
    "https://open.spotify.com/playlist/1cdqXAY5h5yLEdOfsXFqPB?si=24ab156c40f041b2",
    "https://open.spotify.com/playlist/0el0nag6KHK2GVNPNpzgiT?si=94c5580db04642d8",
    "https://open.spotify.com/album/0K7r0Jn2cl3evFj6MFAK2c?si=ToP8gOirTW6OBNeiYBl5DA",
    "https://open.spotify.com/playlist/315NZUnqibdffSXtvldX1e?si=1f46b5c55bd94d72&pt=3012734e169f1183d0f6cca45b55e748",
    "https://open.spotify.com/playlist/51PwhCAZc8EgWUjkKjReUt?si=b606df0a836d4ebf",
    "https://open.spotify.com/album/2qYXlqFxxcrwwyBbTT6nPv?si=cac7be8d445f4723",
    "https://open.spotify.com/playlist/64q8hyjpZX481E91Iw8trN?si=fe63a9a23a7f4ac1",
    "https://open.spotify.com/playlist/6UU5MXh4uouOdN8MjqDWqm?si=25787a1bbff44d14",
    "https://open.spotify.com/playlist/33E0LskXJNzuj8sTzgFPq3?si=95d0f7ddc55f4016",
    "https://open.spotify.com/playlist/3cfHJIShNVAgnImfvigkqe?si=03833f79be29405d",
    "https://open.spotify.com/playlist/1D9Qm2VJkpkasNWSfvZRf1?si=0cf3dc7af47643cb",
    "https://open.spotify.com/playlist/3d0dVNVfu3a2FCs1azIWpy?si=39396ed637354e7e",
    "https://open.spotify.com/playlist/4XzSUYKNatw54F2JZsF63J?si=2eb042f0368a4bf1",
    "https://open.spotify.com/playlist/2zCVcu2EII0EryYRVIp1Tm?si=3312b157f4f04f7d",
    "https://open.spotify.com/playlist/37i9dQZEVXd3l7N59CTBv2?si=c4d7c07f20ee425e",
    "https://open.spotify.com/playlist/1UUHqSb3Krx3UhbNs7XNko?si=b123b068cc9a4821",
    "https://open.spotify.com/playlist/3beIoDL0hgV3meduNQbsmP?si=338f18ce7b3a469d"


]

# Directory where songs will be downloaded
DOWNLOAD_DIR = "spotify_downloads"

def check_dependencies():
    """Check if spotdl and ffmpeg are installed."""
    print("[*] Checking dependencies...")
    
    # Check if spotdl is installed via pip
    try:
        import spotdl
        print("  - spotdl is installed.")
    except ImportError:
        print("  - spotdl is not installed. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "spotdl"])
        print("  - spotdl installed successfully.")

    # Check for ffmpeg (required by spotdl to process audio files)
    ffmpeg_path_win = os.path.expanduser("~/.spotdl/ffmpeg.exe")
    ffmpeg_path_unix = os.path.expanduser("~/.spotdl/ffmpeg")
    
    if shutil.which("ffmpeg") is not None:
        print("  - ffmpeg is installed on system PATH.")
    elif os.path.exists(ffmpeg_path_win) or os.path.exists(ffmpeg_path_unix):
        print("  - ffmpeg is installed locally for spotdl.")
    else:
        print("  - ffmpeg not found.")
        print("    spotdl requires ffmpeg to process audio files.")
        print("    Attempting to download ffmpeg locally for spotdl...")
        try:
            p = subprocess.Popen([sys.executable, "-m", "spotdl", "--download-ffmpeg"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            p.communicate(input='n\n')
            print("  - ffmpeg downloaded successfully.")
        except Exception:
            print("  [!] Failed to download ffmpeg automatically.")
            print("      Please install FFmpeg manually from https://ffmpeg.org/download.html")
            print("      and add it to your system PATH.")
            sys.exit(1)

    # Check for deno (required by yt-dlp to bypass some YouTube restrictions)
    deno_path_win = os.path.expanduser("~/.spotdl/deno.exe")
    deno_path_unix = os.path.expanduser("~/.spotdl/deno")
    if os.path.exists(deno_path_win) or os.path.exists(deno_path_unix) or shutil.which("deno"):
        print("  - Deno is already installed.")
    else:
        print("  - Checking for Deno (required for some YouTube tracks)...")
        try:
            # Use Popen to auto-answer 'n' if it happens to prompt
            p = subprocess.Popen([sys.executable, "-m", "spotdl", "--download-deno"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            p.communicate(input='n\n')
            print("  - Deno is ready.")
        except Exception:
            print("  [!] Failed to download Deno. Some tracks might fail to download.")

def setup_directories():
    """Create download directories if they don't exist."""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    if not os.path.exists(f"{DOWNLOAD_DIR}/Songs"):
        os.makedirs(f"{DOWNLOAD_DIR}/Songs")
    if not os.path.exists(f"{DOWNLOAD_DIR}/Playlists"):
        os.makedirs(f"{DOWNLOAD_DIR}/Playlists")

def download_single_url(url):
    """Download a single Spotify URL."""
    setup_directories()
    print(f"\n[*] Processing URL: {url}")
    try:
        cmd = [
            sys.executable, "-m", "spotdl", "download", url,
            "--output", f"{DOWNLOAD_DIR}/Songs/{{artists}} - {{title}}.{{ext}}",
            "--m3u", f"{DOWNLOAD_DIR}/Playlists/{{list}}.m3u",
            "--overwrite", "skip"
        ]
        
        if url.strip().lower() == "saved":
             cmd = [
                sys.executable, "-m", "spotdl", "saved",
                "--output", f"{DOWNLOAD_DIR}/Songs/{{artists}} - {{title}}.{{ext}}",
                "--m3u", f"{DOWNLOAD_DIR}/Playlists/Liked Songs.m3u",
                "--overwrite", "skip"
             ]
             print("    Note: Downloading 'saved' songs requires you to log in to Spotify.")

        subprocess.check_call(cmd)
        print(f"[*] Successfully finished processing: {url}")
        return True, f"Successfully downloaded: {url}"
        
    except subprocess.CalledProcessError as e:
        print(f"[!] Error downloading {url}: {e}")
        return False, f"Error downloading {url}: {e}"
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
        return False, f"An unexpected error occurred: {e}"

def download_spotify_links():
    """Download the provided Spotify URLs."""
    if not SPOTIFY_URLS:
        print("[!] No URLs provided. Please add your Spotify URLs to the SPOTIFY_URLS list in this file.")
        print("    You can get the link by right-clicking a playlist/song -> Share -> Copy Link.")
        return

    setup_directories()
    print(f"\n[*] Starting download. Files will be saved in: {os.path.abspath(DOWNLOAD_DIR)}")
    
    for url in SPOTIFY_URLS:
        download_single_url(url)

if __name__ == "__main__":
    print("=== Spotify Downloader ===")
    check_dependencies()
    download_spotify_links()
    print("\n=== All downloads completed ===")
