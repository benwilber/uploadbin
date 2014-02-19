uploadbin
=========

uploadbin

run this app somewhere and add this to your local .bashrc

    function uploadbin() {
      local name="$(basename "$1")"
      curl -F "file=@$1;filename=$name" http://uploadbin.sunspot.io/upload
      echo
    }

reload your shell and use like this

    $ uploadbin <file path>
