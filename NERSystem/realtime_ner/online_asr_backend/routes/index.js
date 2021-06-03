const express = require('express')
const router = express.Router()
const MainController = require('../controllers/MainController')
const upload = require('../upload')

router.post('/stream/record', MainController.streamByRecording)

router.post('/stream/import', upload.single('file'), MainController.streamByImport)

module.exports = router
