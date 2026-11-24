#!/usr/bin/env python3
import os
import shutil
import glob
import hashlib

REPO_BTECH = os.path.expanduser("~/git/hereyes-github/B.Tech")
COLLEGE_DIR = os.path.expanduser("~/Downloads/College & Study")
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
DOCS_DIR = os.path.expanduser("~/Documents")

def get_hash(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def collect_repo_hashes():
    hashes = set()
    for root, _, files in os.walk(REPO_BTECH):
        for f in files:
            if not f.startswith("."):
                p = os.path.join(root, f)
                h = get_hash(p)
                if h:
                    hashes.add(h)
    return hashes

def route_file(filename):
    fl = filename.lower()
    if any(k in fl for k in ["iwt", "css", "html", "seo", "web"]):
        if "circular" in fl:
            return os.path.join(REPO_BTECH, "IWT/Circulars")
        return os.path.join(REPO_BTECH, "IWT/Notes_and_Guides")
    elif any(k in fl for k in ["fcs", "linux", "operating_system", "memory", "ssd", "hard_disk", "sbrk", "vmstat", "register", "computer_fundamental", "software_types"]):
        if "circular" in fl:
            return os.path.join(REPO_BTECH, "FCS/Circulars")
        if any(k in fl for k in ["linux", "command", "cp"]):
            return os.path.join(REPO_BTECH, "FCS/Linux_and_Commands")
        if any(k in fl for k in ["operating_system", "os", "memory", "ssd", "hard_disk", "sbrk", "vmstat", "register", "software"]):
            return os.path.join(REPO_BTECH, "FCS/Operating_Systems_and_Hardware")
        return os.path.join(REPO_BTECH, "FCS/Core_Notes_and_Exam_Prep")
    elif any(k in fl for k in ["spc", "loop", "c programming", "c_programming"]):
        if "circular" in fl:
            return os.path.join(REPO_BTECH, "SPC/Circulars")
        return os.path.join(REPO_BTECH, "SPC/Notes_and_Lectures")
    elif any(k in fl for k in ["lac", "derivative", "partial"]):
        if "circular" in fl:
            return os.path.join(REPO_BTECH, "LAC_Mathematics/Circulars")
        return os.path.join(REPO_BTECH, "LAC_Mathematics/Question_Banks")
    elif any(k in fl for k in ["traffic", "iot"]):
        if "circular" in fl:
            return os.path.join(REPO_BTECH, "IoT_and_Projects/Adaptive_Traffic_Light_System")
        return os.path.join(REPO_BTECH, "IoT_and_Projects/Adaptive_Traffic_Light_System")
    elif any(k in fl for k in ["question", "testpad", "mock_test", "mock test", "exam_prep"]):
        return os.path.join(REPO_BTECH, "Questions_and_Assessments/Question_Banks")
    return None

def main():
    if not os.path.exists(REPO_BTECH):
        return

    repo_hashes = collect_repo_hashes()
    transferred = 0

    # 1. Check loose downloads for new circulars and study materials
    for pattern in ["Circular_*.pdf", "*IWT*", "*FCS*", "*SPC*", "*LAC*"]:
        for p in glob.glob(os.path.join(DOWNLOADS_DIR, pattern)):
            if os.path.isfile(p):
                fname = os.path.basename(p)
                dest_dir = route_file(fname)
                if dest_dir:
                    h = get_hash(p)
                    if h and h not in repo_hashes:
                        os.makedirs(dest_dir, exist_ok=True)
                        dest_path = os.path.join(dest_dir, fname)
                        shutil.copy2(p, dest_path)
                        repo_hashes.add(h)
                        transferred += 1
                        print(f"Auto-intake: Copied {fname} -> {os.path.relpath(dest_dir, REPO_BTECH)}")

    # 2. Check College & Study folder for any new files
    if os.path.exists(COLLEGE_DIR):
        for f in os.listdir(COLLEGE_DIR):
            p = os.path.join(COLLEGE_DIR, f)
            if os.path.isfile(p) and not f.startswith("."):
                dest_dir = route_file(f)
                if dest_dir:
                    h = get_hash(p)
                    if h and h not in repo_hashes:
                        os.makedirs(dest_dir, exist_ok=True)
                        dest_path = os.path.join(dest_dir, f)
                        shutil.copy2(p, dest_path)
                        repo_hashes.add(h)
                        transferred += 1
                        print(f"Auto-intake: Copied {f} -> {os.path.relpath(dest_dir, REPO_BTECH)}")

    # 3. Check Documents for Testpad screenshots
    for p in glob.glob(os.path.join(DOCS_DIR, "Screenshot*.png")):
        if os.path.isfile(p):
            fname = os.path.basename(p)
            dest_dir = os.path.join(REPO_BTECH, "Questions_and_Assessments/Chitkara_Testpad_Coding/Screenshots")
            h = get_hash(p)
            if h and h not in repo_hashes:
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, fname)
                shutil.copy2(p, dest_path)
                repo_hashes.add(h)
                transferred += 1
                print(f"Auto-intake: Copied {fname} -> Questions_and_Assessments/Chitkara_Testpad_Coding/Screenshots")

    if transferred > 0:
        print(f"Auto-intake completed: {transferred} new file(s) ingested into B.Tech")

if __name__ == "__main__":
    main()
