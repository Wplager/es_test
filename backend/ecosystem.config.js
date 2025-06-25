module.exports = {
  apps: [{
    name: "flask-app",
    script: "gunicorn",
    args: "-b 127.0.0.1:5000 app:app",
    interpreter: "python3",
    exec_mode: "fork",
    autorestart: true,
    watch: false,
    max_memory_restart: "500M",
    env: {
      NODE_ENV: "production"
    }
  }]
}