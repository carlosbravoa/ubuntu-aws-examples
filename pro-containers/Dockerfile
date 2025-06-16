# 1. Get the token in an env var
# TOKEN=$(sudo pro api u.pro.attach.guest.get_guest_token.v1 | jq -r .data.attributes.guest_token)
# 
#
# 3. Build the containers passing the env var token
# sudo docker build -t my_container --build-arg TOKEN=$TOKEN .


# Download base image ubuntu 22.04
FROM public.ecr.aws/lts/ubuntu:22.04_stable

ARG TOKEN

# LABEL about the custom image
LABEL maintainer="carlos.bravo@canonical.com"
LABEL version="0.1"
LABEL description="This is demo Pro Docker Image for a PHP container running on Ubuntu 22.04 with a Pro subscription. Do not use in production"

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update and install pro client
RUN  apt-get update \
     && apt-get install --no-install-recommends -y \
     ubuntu-advantage-tools ca-certificates

# Attaching the token
RUN pro attach $TOKEN

# upgrade packages
RUN apt-get upgrade -y

# Manually installing apache2 and php modules typically used in a web site (e.g. Wordpress)
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 \
                 php php-bcmath php-curl libapache2-mod-php \
                 php-imagick php-intl php-json php-mbstring php-mysql php-xml \
                 php-zip ghostscript

# Remove the Pro client and clean repos
RUN apt-get purge --auto-remove -y ubuntu-advantage-tools && \
rm -rf /var/lib/apt/lists/*

# Removing index and copying index.php from our local files
RUN rm /var/www/html/index.html
COPY ./index.php /var/www/html/
EXPOSE 80

# Starting apache manually for the demo
CMD /usr/sbin/apache2ctl -D FOREGROUND


