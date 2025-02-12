import psutil

def log_memory_usage():
    process = psutil.Process()
    mem_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    return f"Memory Usage: {mem_usage:.2f} MB"

def log_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent()}%"

def draw_performance_overlay(screen, font, clock):
    process = psutil.Process()
    mem_usage = process.memory_info().rss / (1024 * 1024)  # MB
    cpu_usage = psutil.cpu_percent()
    fps = clock.get_fps()  # Get current FPS
    text = f"FPS: {fps:.2f} | CPU: {cpu_usage}% | Mem: {mem_usage:.2f}MB"
    text_surf = font.render(text, True, (255, 255, 255))
    screen.blit(text_surf, (800, 800))  # Draw in top-left corner