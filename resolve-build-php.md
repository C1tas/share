
sudo cp -r /usr/include/openssl /opt/openssl
sudo cp -r /usr/include/openssl-1.0 /opt/openssl-1.0
sudo rm -rf /usr/include/openssl
sudo cp -r /opt/openssl-1.0/openssl /usr/include/openssl

phpbrew install php-5.6.29 +default +mysql +pdo +debug +fpm +openssl=shared

use the shared option can fix error with the lower version openssl

if without shared option just use old openssl version it does not work 

/home/r7/.phpbrew/build/php-5.6.28/ext/openssl/xp_ssl.c:1646: undefined reference to `sk_num'

/home/r7/.phpbrew/build/php-5.6.28/ext/openssl/xp_ssl.c:1651: undefined reference to `sk_value'

/home/r7/.phpbrew/build/php-5.6.28/ext/openssl/xp_ssl.c:1650: undefined reference to `sk_num'

collect2: error: ld returned 1 exit status

make: *** [Makefile:265: sapi/cli/php] Error 1
