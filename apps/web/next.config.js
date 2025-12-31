/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NODE_ENV === 'development' 
          ? 'http://localhost:4000/api/:path*'
          : '/api/:path*' // In production, this would go to your deployed API
      }
    ];
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NODE_ENV === 'development' 
      ? 'http://localhost:4000'
      : process.env.NEXT_PUBLIC_API_URL,
  }
}

module.exports = nextConfig
