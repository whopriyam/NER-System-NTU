// a small middleware for uploading file

const multer = require('multer')
const path = require('path')
const crypto = require('crypto')

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'storage/')
  },
  filename: (req, file, cb) => {
    if (['.wav', '.mp3', '.mp4'].includes(path.extname(file.originalname))) {
      cb(null, `${crypto.randomBytes(3).toString('hex')}${Date.now()}${path.extname(file.originalname)}`)
    } else {
      return cb(new Error('File type is not supported! Only WAV, MP3 and MP4 are allowed'))
    }
  }
})
const upload = multer({ storage: storage })

module.exports = upload
