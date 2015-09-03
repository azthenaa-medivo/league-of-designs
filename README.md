# League of Designs
We shall discuss the designs of our wonderful world of League of Legends. Because we're nice and all.

# About

This is a simple, almost static website which sorts Red Posts for you ! You can look at the source code on GitHub
and yell at me because I'm not doing any caching *yet*.

* LoD regularly collects Red Posts from Riot's Board and sort them by Champion, Rioter, etc.
* You may also read some chilled Articles.
* I avoid Mongoengine because it's never worked properly withotu tons of monkey patching... So yes I take care of
everything myself.

# Requirements

* Python    3.2
* Django	1.8
* Markdown	2.6
    * Markdown Superscript
* Pymongo	3.0
* Requests	2.7