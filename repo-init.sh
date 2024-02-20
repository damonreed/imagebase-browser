##
## repo-init.sh
##
export REPO="imagebase-browser"
export DESC="A simple browser for the imagebase AI image database"
gh repo create $REPO -d "$DESC" --public
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:damonreed/${REPO}.git
git push -u origin main