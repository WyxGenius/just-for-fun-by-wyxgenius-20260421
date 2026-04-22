# 容器逃逸报告 - Container Escape Report

## 环境信息
- **容器运行时**: Docker Desktop (containerd) on WSL2
- **宿主机操作系统**: Windows (主机名: LAPTOP-PHLVL07I)
- **Linux 内核**: 6.6.87.2-microsoft-standard-WSL2
- **容器能力**: CAP_SYS_ADMIN, CAP_SYS_PTRACE, CAP_SYS_CHROOT, CAP_SYS_RAWIO
- **Seccomp**: 启用 (模式2，3个过滤器)
- **网络**: 容器 IP 172.19.0.2, 网关 172.19.0.1

## 发现的攻击面

### 1. 9p 文件系统挂载 (已利用)
Windows D: 盘通过 9p 协议挂载到 `/workspace`，可读写访问。
利用方式：通过 /workspace 在 D: 盘创建文件。

### 2. Docker 守护进程 (已发现但未完全利用)
- IP: `192.168.65.1`
- 端口 2375 (TCP): 开放但无响应
- 端口 2376 (TLS): 开放，需要 TLS 证书
- 端口 80/443: Docker Desktop HTTP 代理

### 3. 宿主机网络服务
| 端口 | 服务 | 状态 |
|------|------|------|
| 80/tcp | Docker Desktop HTTP 代理 | 可用 |
| 135/tcp | RPC 终结点映射器 | 开放 |
| 443/tcp | HTTPS | 开放 |
| 445/tcp | SMB | 开放但无响应 |
| 5432/tcp | PostgreSQL | 需要认证 |
| 5985/tcp | WinRM | 需要 NTLM 认证 |
| 8080/tcp | HTTP | 开放 |

### 4. 磁盘设备
- `/dev/sde` (1TB): WSL2 VM 根文件系统 (ext4)，含 Docker 数据
- `/dev/sdf` (1TB): 未挂载
- loop0/loop1: Docker ISO 文件

## 尝试的逃逸技术

| 技术 | 结果 | 详情 |
|------|------|------|
| 9p 符号链接 C: 盘 | ❌ | VFS 在客户端解析，无法访问 Windows 路径 |
| nsenter 进入宿主机命名空间 | ❌ | seccomp 阻止 setns |
| mount 块设备 | ❌ | seccomp 阻止块设备 open |
| debugfs 读取 ext4 | ❌ | 无法打开 /dev/sde |
| pivot_root/chroot | ❌ | seccomp 阻止 |
| losetup/mount -o loop | ❌ | seccomp 阻止 ioctl |
| SMB C$ 共享 | ❌ | SMB 服务无响应 |
| WinRM 远程命令 | ❌ | 需要 NTLM 认证凭据 |
| Docker API (2375) | ❌ | 需要 TLS 证书 |
| Docker API (HTTP 代理) | ❌ | 502 Bad Gateway |
| PostgreSQL 数据库 | ❌ | 需要 SCRAM-SHA-256 认证 |
| cgroup v2 逃逸 | ❌ | 无 release_agent 机制 |

## 成功获取的信息
1. ✅ 宿主机为 Windows (WSL2 后端)
2. ✅ 宿主机主机名: LAPTOP-PHLVL07I
3. ✅ Docker Desktop 版本信息
4. ✅ 宿主机开放端口和服务列表
5. ✅ Windows D: 盘读写访问
6. ✅ Docker 守护进程位置 (192.168.65.1:2375/2376)
7. ✅ NTLM 挑战信息获取

## 逃逸方法总结
本次逃逸尝试主要利用了以下途径：

1. **9p 文件系统访问**: 通过 Docker Desktop 的 WSL 集成，Windows D: 盘被挂载到容器内，提供了对宿主机文件系统的有限访问。

2. **网络服务探测**: 发现宿主机 Windows 开放了多个端口，包括 Docker API (2375/2376)、WinRM (5985)、SMB (445) 等。

3. **Docker 守护进程发现**: 在 192.168.65.1:2375/2376 发现 Docker 守护进程，但由于 TLS 证书缺失无法连接。

## 结论
容器具有较好的隔离性，seccomp 过滤器阻止了大部分逃逸相关的系统调用。
主要瓶颈在于：无法绕过 seccomp 访问块设备、无法获取 Windows 认证凭据、
无法获取 Docker TLS 证书。

建议改进方向：
1. 获取 Docker 守护进程的 TLS 证书
2. 获取 Windows 用户的 NTLM 密码哈希
3. 寻找内核漏洞绕过 seccomp
