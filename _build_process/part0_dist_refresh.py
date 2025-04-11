import os
import shutil

def reset_dist(reset_flag=True):
    """
    Resets the 'dist' directory using 'dist_fresh'. 
    If 'dist_fresh' does not exist, it is created as a copy of 'dist'.
    
    If reset_flag is True, the function removes 'dist' 
    and then copies 'dist_fresh' into 'dist'.
    
    Parameters:
      reset_flag (bool): If True, perform the reset.
    """
    abs_path = '/Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025'
    dist = os.path.join(abs_path, 'dist')
    dist_fresh = os.path.join(abs_path, 'dist_fresh')
    
    # Create a backup copy of dist if dist_fresh doesn't exist.
    if not os.path.exists(dist_fresh):
        print(f"Creating backup directory 'dist_fresh' from {dist}...")
        shutil.copytree(dist, dist_fresh)
    else:
        print(f"'dist_fresh' already exists. Proceeding with reset if requested.")
    
    if reset_flag:
        if os.path.exists(dist):
            print(f"Removing existing 'dist' directory...")
            shutil.rmtree(dist)
        print(f"Copying 'dist_fresh' to 'dist'...")
        shutil.copytree(dist_fresh, dist)
        print("Reset of 'dist' complete.")
    else:
        print("Reset flag is disabled. No changes made.")

# Example of calling the function:
if __name__ == '__main__':
    reset_dist(reset_flag=True)
