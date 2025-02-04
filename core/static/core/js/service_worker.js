// 例: Workboxライブラリの読み込み（CDNから読み込む場合）
importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.5.4/workbox-sw.js');

// 次の0時までの秒数を計算する関数
const secondsUntilMidnight = () => {
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  tomorrow.setHours(0, 0, 0, 0);
  return Math.floor((tomorrow.getTime() - now.getTime()) / 1000);
};

// index.htmlに対して NetworkFirst 戦略を利用し、キャッシュの有効期限を動的に設定
workbox.routing.registerRoute(
  ({ url }) => url.pathname === '/index.html',
  new workbox.strategies.NetworkFirst({
    cacheName: 'dynamic-index',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxAgeSeconds: secondsUntilMidnight(),
      }),
    ],
  })
);

// その他のキャッシュ戦略やイベントハンドラなどを記述
self.addEventListener('fetch', function(event) {});
