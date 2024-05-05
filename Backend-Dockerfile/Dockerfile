FROM 211125489433.dkr.ecr.us-east-2.amazonaws.com/php-base-image

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer --version=2.6.0

WORKDIR /leadsverificationsystem/backend
COPY . .

RUN composer install

RUN service nginx start

#Configure Supervisor to run php artisan serve
RUN echo "[program:laravel]" >> /etc/supervisor/conf.d/laravel.conf && \
    echo "command=php artisan serve --host=0.0.0.0" >> /etc/supervisor/conf.d/laravel.conf && \
    echo "directory=/leadsverificationsystem/backend" >> /etc/supervisor/conf.d/laravel.conf && \
    echo "autostart=true" >> /etc/supervisor/conf.d/laravel.conf && \
    echo "autorestart=true" >> /etc/supervisor/conf.d/laravel.conf


#configure nginx
RUN sed -i 's@try_files \$uri \$uri/ =404;@proxy_pass http://localhost:8000;@g' /etc/nginx/sites-enabled/default

RUN service nginx start


EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


#php artisan migrate
#php artisan passport:install
#service supervisor start
