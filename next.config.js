/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  basePath: '/RealTimeStudentSuccessPredictionSystem',
  assetPrefix: '/RealTimeStudentSuccessPredictionSystem',
  trailingSlash: true,
}

module.exports = nextConfig 