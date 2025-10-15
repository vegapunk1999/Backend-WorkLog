import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def setup_logging(
    app_name: str = "app",
    logs_dir: str | Path | None = None,
    keep_days: int = 30,
    level: int = logging.INFO,
) -> Path:
    """
    Pasang root logger:
    - Tulis ke file logs/<app_name>.log
    - Rotate tiap midnight jadi <app_name>.log.YYYY-MM-DD
    - Simpan arsip log sampai keep_days
    - Juga tampilkan di console
    """
    logs_path = (
        Path(logs_dir) if logs_dir else Path(__file__).resolve().parent.parent / "logs"
    )
    logs_path.mkdir(parents=True, exist_ok=True)
    log_file = logs_path / f"{app_name}.log"

    fmt = "%(asctime)s %(levelname)s [%(name)s]: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"  # pakai local time (Asia/Jakarta kalau OS-nya diset)

    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        interval=1,
        backupCount=keep_days,
        encoding="utf-8",
        utc=False,  # biar pakai waktu lokal
        delay=True,  # file dibuat saat pertama kali dipakai
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    root = logging.getLogger()
    root.setLevel(level)

    # hindari duplikasi handler saat dipanggil berulang
    for h in root.handlers[:]:
        root.removeHandler(h)

    root.addHandler(file_handler)
    root.addHandler(console_handler)

    # toning down noisy libs kalau perlu
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.INFO)
    logging.getLogger("apscheduler").setLevel(logging.INFO)

    return log_file
