upstream demo {
    server ${APP_HOST}:${APP_PORT};
}
upstream socks {
    server ${APP_HOST}:${WS_PORT};
}


server {
    listen ${LISTEN_PORT};
    server_name main.com ns.main.com *.main.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location / {
        proxy_pass http://demo;
        client_max_body_size    5M;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }

    location /static {
        alias /vol/static;
    }

    location /socket/ {
        proxy_pass http://socks;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;

    }
}


