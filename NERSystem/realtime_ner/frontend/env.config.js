const prod = process.env.NODE_ENV === "production";

module.exports = {
  "process.env.HIGHLIGHTER_BACKEND_URL": prod
    ? "ws://155.69.146.209/atc_highlighter-service/"
    : "ws://localhost:5000/",
  "process.env.ASR_BACKEND_URL": "ws://155.69.146.209:8888/client/ws/speech",
  "process.env.ASR_BACKEND_STATUS_URL":
    "ws://155.69.146.209:8888/client/ws/status"
};
