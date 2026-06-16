FROM httpd:2.4-alpine

RUN apk add --no-cache apache2-proxy apache2-ssl

COPY rtvoyage.conf /usr/local/apache2/conf/extra/rtvoyage.conf

RUN echo "Include conf/extra/rtvoyage.conf" >> /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule proxy_module/LoadModule proxy_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule proxy_http_module/LoadModule proxy_http_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule rewrite_module/LoadModule rewrite_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule headers_module/LoadModule headers_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule deflate_module/LoadModule deflate_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule expires_module/LoadModule expires_module/' /usr/local/apache2/conf/httpd.conf

EXPOSE 80
