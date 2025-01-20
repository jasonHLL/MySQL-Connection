import os
import time
import subprocess
import schedule

# 配置数据库和备份信息
DB_HOST = '101.35.46.20'
DB_USER = 'root'
DB_PASSWORD = 'Your0Password!'
DB_NAME = 'Software_Registration'
BACKUP_DIR = r'C:\Users\Jason\Desktop\SQL_database 备份'

def backup_database():
    # 确保备份目录存在
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # 生成备份文件名，包含时间戳
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'{DB_NAME}_backup_{timestamp}.sql')

    # 使用 mysqldump 进行备份
    dump_cmd = f"mysqldump -h {DB_HOST} -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {backup_file}"
    try:
        subprocess.run(dump_cmd, shell=True, check=True)
        print(f"Backup completed: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")

# schedule.every(1).minutes.do(backup_database)


# 立即测试备份
if __name__ == "__main__":
    print("开始运行备份...")
    backup_database()