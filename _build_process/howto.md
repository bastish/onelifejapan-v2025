0. delete dist + dist_fresh

1. npm run build
   Was going to fast for server so used
   import { limitedFetch } from './limitedFetch';

2. source env/bin/activate

# Collect images

3. python3 /Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/\_build_process/part1_collect_images.py

# Resize / optimize images

4. python3 /Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/\_build_process/part2_optimize_images.py

# rewrite image src paths to webp

5. python3 /Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/\_build_process/part3_change_paths_to_webp.py

# Remove heavy jpgs

6. python3 /Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/\_build_process/part4_delete_source_images.py

# remove dev only pages

7. python3 /Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/\_build_process/part5_remove_dev_only_pages.py

############
OK

CHECK IT on local to make sure images / etc

python3 -m http.server 8005 --directory dist

<!-- cd dist
python3 -m http.server 8005 -->

<!-- Branch Definitions
main (or master):
The primary branch containing the stable and production-ready code.

stage (or staging):
A branch used for testing and quality assurance before changes are merged into main. It reflects a pre-production environment where you can validate new features.

deploy (or deploy-branch):
A dedicated branch for deployment purposes. It can be the same as stage or a separate branch depending on your workflow.

production (or live):
Sometimes used interchangeably with main, but in some workflows, it's a separate branch reflecting the live site. -->

## (ONE TIME ONLY)

## cd /Users/kevincameron/Documents/onelifejapan_static_2023/onelifejapan.com-deployed-site

## open /Users/kevincameron/Documents/OLJDevProjects/OLJVercelDeploy

## git clone https://github.com/bastish/onelifejapan.com-deployed.git

## 👆 Only do this once. After that, re-use the local clone!

cd /Users/kevincameron/Documents/OLJDevProjects/OLJVercelDeploy/onelifejapan.com-deployed

# ✅ Update the local repo instead of recloning

git checkout stage
git pull origin stage

- checkout stage
  git checkout stage

# 🧹 Clean old dist dir

rm -rf dist

# 📁 Copy new dist

cp -r /Users/kevincameron/Documents/OLJDevProjects/onelifejapan-v2025/dist dist

# 🔄 Commit and push to stage

git add dist
git commit -m "Deploy [updated family landing google day 2] for stage"
git push origin stage

# 🔎 Check Vercel

# https://vercel.com/kevin-camerons-projects/onelifejapan-com-deployed/deployments

# 🚀 Promote to production

git checkout master
git pull origin master # ✅ add this just in case master was updated elsewhere

rm -rf dist/
git checkout stage -- dist/
git add dist/
git commit -m " Update Production [updated family landing google day 2]"
git push origin master

# 🧽 Optional clean up (safe but slow)

# git gc --prune=now --aggressive

####################
####################
####################
####################

GIT HUB PAGES

cd /path/to/onelifejapan.com-deployed
git checkout -b gh-pages
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages

###

- archive past branches
  on featurebranch
  git checkout feature/blog-from-api

git checkout master
git pull origin master (optional)
git merge feature/blog-from-api
git push origin master

cahnge name
git branch -m feature/blog-from-api archive/blog-from-api
git push origin archive/blog-from-api
git branch -r
git push origin --delete feature/blog-from-api
