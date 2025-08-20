git pull

npm i
pm2 stop solid_docs
pm2 start solid_docs
tail -100f ~/.pm2/logs/solid-docs-out.log