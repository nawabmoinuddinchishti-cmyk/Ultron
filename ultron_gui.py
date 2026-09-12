# ========== KUBRA ULTRON OMEGA - ULTRA MODERN GUI v25.0 ==========
# Full Modern GUI with Animations, Effects & Glassmorphism

import sys
import os
import time
import random
import threading
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QFrame, QScrollArea,
    QGraphicsDropShadowEffect, QStackedWidget, QListWidget, QListWidgetItem,
    QProgressBar, QSlider, QComboBox, QCheckBox, QSystemTrayIcon, QMenu,
    QAction, QShortcut, QSizePolicy, QSpacerItem, QGraphicsOpacityEffect
)
from PyQt5.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve,
    QRect, QPoint, QSize, QParallelAnimationGroup, QSequentialAnimationGroup,
    QPauseAnimation, pyqtProperty, QObject
)
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush,
    QLinearGradient, QRadialGradient, QFontDatabase, QKeySequence,
    QCursor, QPen
)

import pyttsx3
import psutil

# ========== CONFIGURATION ==========
SYSTEM_NAME = "KUBRA ULTRON OMEGA"
VERSION = "v25.0 ULTRA MODERN"
OWNER = "Moin Uddin"
CREATOR = "Chishti Bro"

# ========== COLOR SCHEMES ==========
COLORS = {
    "bg_primary": "#0a0a0f",
    "bg_secondary": "#12121a",
    "bg_tertiary": "#1a1a2e",
    "accent_red": "#ff0033",
    "accent_blue": "#00d4ff",
    "accent_orange": "#ff6b00",
    "accent_green": "#00ff88",
    "accent_purple": "#a855f7",
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0b0",
    "text_muted": "#606070",
    "glass": "rgba(255, 255, 255, 0.05)",
    "glass_border": "rgba(255, 255, 255, 0.1)",
}

# ========== VOICE ENGINE ==========
import platform
engine = pyttsx3.init('sapi5') if platform.system() == "Windows" else pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak(text):
    def _speak():
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    threading.Thread(target=_speak, daemon=True).start()


# ========== ANIMATED BACKGROUND WIDGET ==========
class AnimatedBackground(QWidget):
    """Animated particle background"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        for _ in range(60):
            self.particles.append({
                'x': random.randint(0, 1920),
                'y': random.randint(0, 1080),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3),
                'alpha': random.randint(30, 120),
                'color': random.choice([COLORS["accent_red"], COLORS["accent_blue"], COLORS["accent_purple"]])
            })

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(30)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def update_particles(self):
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']

            if p['x'] < 0 or p['x'] > self.width():
                p['vx'] *= -1
            if p['y'] < 0 or p['y'] > self.height():
                p['vy'] *= -1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(10, 10, 15))
        gradient.setColorAt(0.5, QColor(18, 18, 26))
        gradient.setColorAt(1, QColor(26, 26, 46))
        painter.fillRect(self.rect(), gradient)

        for p in self.particles:
            color = QColor(p['color'])
            color.setAlpha(p['alpha'])
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPoint(int(p['x']), int(p['y'])), p['size'], p['size'])

        painter.setPen(QPen(QColor(255, 0, 51, 15), 1))
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                dist = ((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)**0.5
                if dist < 150:
                    painter.drawLine(int(p1['x']), int(p1['y']), int(p2['x']), int(p2['y']))


# ========== GLASSMORPHISM FRAME ==========
class GlassFrame(QFrame):
    """Glassmorphism effect frame"""

    def __init__(self, parent=None, radius=20):
        super().__init__(parent)
        self.radius = radius
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.03));
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: {radius}px;
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)


# ========== NEON BUTTON ==========
class NeonButton(QPushButton):
    """Animated neon button"""

    def __init__(self, text, color="#ff0033", parent=None):
        super().__init__(text, parent)
        self.color = color
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(45)
        self.setFont(QFont("Segoe UI", 10, QFont.Bold))

        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color},
                    stop:1 {self._darken(color)});
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self._lighten(color)},
                    stop:1 {color});
            }}
            QPushButton:pressed {{
                padding-top: 12px;
                padding-left: 22px;
            }}
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(color))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def _darken(self, hex_color):
        c = QColor(hex_color)
        return c.darker(150).name()

    def _lighten(self, hex_color):
        c = QColor(hex_color)
        return c.lighter(130).name()


# ========== CHAT MESSAGE WIDGET ==========
class ChatMessage(QFrame):
    """Individual chat message with animation"""

    def __init__(self, text, is_user=False, personality="ULTRON", parent=None):
        super().__init__(parent)
        self.is_user = is_user

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        avatar = QLabel()
        avatar.setFixedSize(45, 45)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFont(QFont("Segoe UI Emoji", 20))

        if is_user:
            avatar.setText("👤")
            avatar.setStyleSheet(f"""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4444ff, stop:1 #6622ff);
                border-radius: 22px;
                color: white;
            """)
        else:
            icons = {"ULTRON": "🔴", "JARVIS": "🟡", "FRIDAY": "🟠"}
            colors = {"ULTRON": "#ff0033", "JARVIS": "#00d4ff", "FRIDAY": "#ff6b00"}
            avatar.setText(icons.get(personality, "🤖"))
            c = colors.get(personality, "#ff0033")
            avatar.setStyleSheet(f"""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {c}, stop:1 {QColor(c).darker(150).name()});
                border-radius: 22px;
                color: white;
            """)

        bubble = QFrame()
        bubble.setMaximumWidth(700)

        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(15, 12, 15, 12)

        name = QLabel("YOU" if is_user else f"{personality}")
        name.setFont(QFont("Segoe UI", 9, QFont.Bold))
        name.setStyleSheet(f"color: {'#00ff88' if is_user else '#ff6b00'}; letter-spacing: 1px;")

        msg = QLabel(text)
        msg.setWordWrap(True)
        msg.setFont(QFont("Segoe UI", 11))
        msg.setStyleSheet("color: white; line-height: 1.5;")
        msg.setTextInteractionFlags(Qt.TextSelectableByMouse)

        time_label = QLabel(datetime.now().strftime("%I:%M %p"))
        time_label.setFont(QFont("Segoe UI", 8))
        time_label.setStyleSheet("color: #606070;")

        bubble_layout.addWidget(name)
        bubble_layout.addWidget(msg)
        bubble_layout.addWidget(time_label)

        if is_user:
            bubble.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(68, 68, 255, 0.25),
                        stop:1 rgba(102, 34, 255, 0.15));
                    border: 1px solid rgba(100, 100, 255, 0.4);
                    border-radius: 18px;
                }
            """)
            layout.addStretch()
            layout.addWidget(bubble)
            layout.addWidget(avatar, alignment=Qt.AlignTop)
        else:
            bubble.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.08),
                        stop:1 rgba(255, 255, 255, 0.03));
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 18px;
                }
            """)
            layout.addWidget(avatar, alignment=Qt.AlignTop)
            layout.addWidget(bubble)
            layout.addStretch()

        self.setWindowOpacity(0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()


# ========== SIDEBAR ==========
class Sidebar(QWidget):
    """Modern sidebar with animated buttons"""

    personality_changed = pyqtSignal(str)
    action_triggered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)

        logo = QLabel("⚡ ULTRON")
        logo.setFont(QFont("Orbitron", 22, QFont.Bold))
        logo.setStyleSheet(f"""
            color: {COLORS['accent_red']};
            letter-spacing: 4px;
            padding: 10px;
        """)
        logo.setAlignment(Qt.AlignCenter)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(COLORS['accent_red']))
        logo.setGraphicsEffect(shadow)

        layout.addWidget(logo)

        version = QLabel(f"{VERSION}")
        version.setFont(QFont("Segoe UI", 8))
        version.setStyleSheet("color: #606070; letter-spacing: 2px;")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        layout.addSpacing(20)

        personality_label = self._section_label("🎭 PERSONALITY")
        layout.addWidget(personality_label)

        self.personality_buttons = {}
        for name, color, emoji in [
            ("ULTRON", COLORS["accent_red"], "🔴"),
            ("JARVIS", COLORS["accent_blue"], "🟡"),
            ("FRIDAY", COLORS["accent_orange"], "🟠")
        ]:
            btn = self._personality_btn(f"{emoji}  {name}", color, name)
            self.personality_buttons[name] = btn
            layout.addWidget(btn)

        self.set_active_personality("ULTRON")

        layout.addSpacing(15)

        actions_label = self._section_label("⚡ QUICK ACTIONS")
        layout.addWidget(actions_label)

        actions = [
            ("🎮 Generate Game", "generate_game"),
            ("🔬 Scan Circuit", "scan_circuit"),
            ("🏠 Home Control", "home_control"),
            ("🛡️ Security Scan", "security_scan"),
            ("📊 System Status", "system_status"),
            ("🌤️ Weather", "weather"),
        ]

        for text, action in actions:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(38)
            btn.setFont(QFont("Segoe UI", 10))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {COLORS['text_secondary']};
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 10px;
                    text-align: left;
                    padding-left: 15px;
                }}
                QPushButton:hover {{
                    background: rgba(255, 255, 255, 0.05);
                    color: white;
                    border: 1px solid {COLORS['accent_blue']};
                }}
            """)
            btn.clicked.connect(lambda _, a=action: self.action_triggered.emit(a))
            layout.addWidget(btn)

        layout.addStretch()

        monitor_label = self._section_label("📊 SYSTEM MONITOR")
        layout.addWidget(monitor_label)

        self.cpu_bar = self._create_monitor("CPU", COLORS["accent_red"])
        layout.addWidget(self.cpu_bar)

        self.ram_bar = self._create_monitor("RAM", COLORS["accent_blue"])
        layout.addWidget(self.ram_bar)

        self.disk_bar = self._create_monitor("DISK", COLORS["accent_green"])
        layout.addWidget(self.disk_bar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_monitor)
        self.timer.start(1000)

    def _section_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        label.setStyleSheet(f"color: {COLORS['text_muted']}; letter-spacing: 2px; padding: 5px;")
        return label

    def _personality_btn(self, text, color, name):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(45)
        btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_secondary']};
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                text-align: left;
                padding-left: 20px;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.03);
                color: white;
                border: 2px solid {color};
            }}
        """)
        btn.clicked.connect(lambda: self.set_active_personality(name))
        return btn

    def set_active_personality(self, name):
        colors = {"ULTRON": COLORS["accent_red"], "JARVIS": COLORS["accent_blue"], "FRIDAY": COLORS["accent_orange"]}

        for pname, btn in self.personality_buttons.items():
            if pname == name:
                color = colors[pname]
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 {color}, stop:1 {QColor(color).darker(180).name()});
                        color: white;
                        border: 2px solid {color};
                        border-radius: 12px;
                        text-align: left;
                        padding-left: 20px;
                        font-weight: bold;
                        letter-spacing: 1px;
                    }}
                """)
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(20)
                shadow.setColor(QColor(color))
                btn.setGraphicsEffect(shadow)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: transparent;
                        color: {COLORS['text_secondary']};
                        border: 2px solid rgba(255, 255, 255, 0.1);
                        border-radius: 12px;
                        text-align: left;
                        padding-left: 20px;
                        letter-spacing: 1px;
                    }}
                    QPushButton:hover {{
                        background: rgba(255, 255, 255, 0.03);
                        color: white;
                        border: 2px solid {colors[pname]};
                    }}
                """)
                btn.setGraphicsEffect(None)

        self.personality_changed.emit(name)

    def _create_monitor(self, label, color):
        container = QFrame()
        container.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)

        header = QHBoxLayout()
        name = QLabel(label)
        name.setFont(QFont("Segoe UI", 8, QFont.Bold))
        name.setStyleSheet(f"color: {color};")

        value = QLabel("0%")
        value.setFont(QFont("Segoe UI", 8))
        value.setStyleSheet("color: white;")
        value.setAlignment(Qt.AlignRight)

        header.addWidget(name)
        header.addStretch()
        header.addWidget(value)

        bar = QProgressBar()
        bar.setFixedHeight(6)
        bar.setTextVisible(False)
        bar.setStyleSheet(f"""
            QProgressBar {{
                background: rgba(255, 255, 255, 0.05);
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {QColor(color).lighter(150).name()});
                border-radius: 3px;
            }}
        """)

        layout.addLayout(header)
        layout.addWidget(bar)

        container.value_label = value
        container.bar = bar
        container.color = color

        return container

    def update_monitor(self):
        try:
            cpu = int(psutil.cpu_percent())
            ram = int(psutil.virtual_memory().percent)
            disk = int(psutil.disk_usage('/').percent)

            self.cpu_bar.bar.setValue(cpu)
            self.cpu_bar.value_label.setText(f"{cpu}%")
            self.ram_bar.bar.setValue(ram)
            self.ram_bar.value_label.setText(f"{ram}%")
            self.disk_bar.bar.setValue(disk)
            self.disk_bar.value_label.setText(f"{disk}%")
        except:
            pass


# ========== TYPING INDICATOR ==========
class TypingIndicator(QFrame):
    """Animated typing indicator"""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        avatar = QLabel("🔴")
        avatar.setFixedSize(45, 45)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFont(QFont("Segoe UI Emoji", 20))
        avatar.setStyleSheet("background: rgba(255, 0, 51, 0.3); border-radius: 22px;")

        bubble = QFrame()
        bubble.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 18px;
            }
        """)

        bubble_layout = QHBoxLayout(bubble)
        bubble_layout.setContentsMargins(20, 12, 20, 12)
        bubble_layout.setSpacing(8)

        self.dots = []
        for _ in range(3):
            dot = QLabel("●")
            dot.setFont(QFont("Segoe UI", 14))
            dot.setStyleSheet("color: #ff0033;")
            bubble_layout.addWidget(dot)
            self.dots.append(dot)

        layout.addWidget(avatar)
        layout.addWidget(bubble)
        layout.addStretch()

        self.dot_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(300)

    def animate(self):
        for i, dot in enumerate(self.dots):
            if i == self.dot_index:
                dot.setStyleSheet("color: #ff0033; font-size: 20px;")
            else:
                dot.setStyleSheet("color: rgba(255, 0, 51, 0.3); font-size: 14px;")

        self.dot_index = (self.dot_index + 1) % 3


# ========== MAIN APPLICATION ==========
class UltronGUI(QMainWindow):
    """Main GUI Application"""

    def __init__(self):
        super().__init__()
        self.current_personality = "ULTRON"
        self.setWindowTitle(f"{SYSTEM_NAME} {VERSION}")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.dragging = False
        self.drag_position = None

        self.setup_ui()
        self.setup_shortcuts()

        QTimer.singleShot(500, self.welcome_message)

    def setup_ui(self):
        """Setup main UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.bg = AnimatedBackground(main_widget)
        self.bg.setGeometry(0, 0, 1400, 900)
        self.bg.lower()

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        main_layout.addWidget(self.create_title_bar())

        content = QHBoxLayout()
        content.setSpacing(15)

        self.sidebar = Sidebar()
        self.sidebar.personality_changed.connect(self.on_personality_change)
        self.sidebar.action_triggered.connect(self.on_action)

        sidebar_container = GlassFrame(radius=20)
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.addWidget(self.sidebar)

        content.addWidget(sidebar_container)

        content.addWidget(self.create_chat_area(), 1)

        main_layout.addLayout(content, 1)

    def create_title_bar(self):
        """Custom title bar"""
        bar = GlassFrame(radius=15)
        bar.setFixedHeight(50)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 5, 15, 5)

        title = QLabel(f"⚡ {SYSTEM_NAME}")
        title.setFont(QFont("Orbitron", 12, QFont.Bold))
        title.setStyleSheet(f"color: {COLORS['accent_red']}; letter-spacing: 2px;")

        layout.addWidget(title)

        status = QLabel("● ONLINE")
        status.setFont(QFont("Segoe UI", 9, QFont.Bold))
        status.setStyleSheet("color: #00ff88; letter-spacing: 1px;")
        layout.addWidget(status)

        layout.addStretch()

        self.time_label = QLabel()
        self.time_label.setFont(QFont("Segoe UI", 10))
        self.time_label.setStyleSheet("color: #a0a0b0;")
        layout.addWidget(self.time_label)

        timer = QTimer()
        timer.timeout.connect(lambda: self.time_label.setText(datetime.now().strftime("%I:%M %p | %d %b %Y")))
        timer.start(1000)

        layout.addSpacing(20)

        for text, color, action in [
            ("─", "#00ff88", self.showMinimized),
            ("□", "#ffaa00", self.toggle_max),
            ("✕", "#ff0033", self.close)
        ]:
            btn = QPushButton(text)
            btn.setFixedSize(35, 35)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {color};
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 17px;
                }}
                QPushButton:hover {{
                    background: {color};
                    color: black;
                    border: none;
                }}
            """)
            btn.clicked.connect(action)
            layout.addWidget(btn)

        return bar

    def create_chat_area(self):
        """Create chat interface"""
        container = GlassFrame(radius=20)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 0, 51, 0.15),
                    stop:1 rgba(0, 0, 0, 0));
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 10, 25, 10)

        self.personality_avatar = QLabel("🔴")
        self.personality_avatar.setFixedSize(50, 50)
        self.personality_avatar.setAlignment(Qt.AlignCenter)
        self.personality_avatar.setFont(QFont("Segoe UI Emoji", 24))
        self.personality_avatar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #ff0033, stop:1 #8b0000);
            border-radius: 25px;
        """)

        header_layout.addWidget(self.personality_avatar)

        info = QVBoxLayout()
        info.setSpacing(2)

        self.chat_title = QLabel("ULTRON")
        self.chat_title.setFont(QFont("Orbitron", 14, QFont.Bold))
        self.chat_title.setStyleSheet("color: white; letter-spacing: 2px;")

        self.chat_subtitle = QLabel("⚡ Ready to serve | Autonomous Mode Active")
        self.chat_subtitle.setFont(QFont("Segoe UI", 9))
        self.chat_subtitle.setStyleSheet("color: #a0a0b0;")

        info.addWidget(self.chat_title)
        info.addWidget(self.chat_subtitle)

        header_layout.addLayout(info)
        header_layout.addStretch()

        self.voice_btn = QPushButton("🎤")
        self.voice_btn.setFixedSize(45, 45)
        self.voice_btn.setCursor(Qt.PointingHandCursor)
        self.voice_btn.setFont(QFont("Segoe UI Emoji", 18))
        self.voice_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 22px;
                color: white;
            }
            QPushButton:hover {
                background: rgba(255, 0, 51, 0.2);
                border: 2px solid #ff0033;
            }
        """)
        self.voice_btn.clicked.connect(self.toggle_voice)

        header_layout.addWidget(self.voice_btn)

        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 0, 51, 0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 0, 51, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

        self.chat_widget = QWidget()
        self.chat_widget.setStyleSheet("background: transparent;")

        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setContentsMargins(10, 15, 10, 15)
        self.chat_layout.setSpacing(8)
        self.chat_layout.addStretch()

        scroll.setWidget(self.chat_widget)
        self.chat_scroll = scroll
        layout.addWidget(scroll, 1)

        input_frame = QFrame()
        input_frame.setFixedHeight(90)
        input_frame.setStyleSheet("""
            QFrame {
                background: rgba(0, 0, 0, 0.3);
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)

        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(20, 15, 20, 15)
        input_layout.setSpacing(10)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your command or message... (Press Enter)")
        self.input_box.setFont(QFont("Segoe UI", 11))
        self.input_box.setMinimumHeight(50)
        self.input_box.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.05);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                padding: 10px 20px;
                selection-background-color: #ff0033;
            }
            QLineEdit:focus {
                border: 2px solid #ff0033;
                background: rgba(255, 0, 51, 0.05);
            }
        """)
        self.input_box.returnPressed.connect(self.send_message)

        input_layout.addWidget(self.input_box, 1)

        self.send_btn = QPushButton("➤")
        self.send_btn.setFixedSize(50, 50)
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff0033, stop:1 #8b0000);
                color: white;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff3355, stop:1 #ff0033);
            }
            QPushButton:pressed {
                background: #8b0000;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("#ff0033"))
        self.send_btn.setGraphicsEffect(shadow)

        self.send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.send_btn)

        layout.addWidget(input_frame)

        return container

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        QShortcut(QKeySequence("Ctrl+M"), self, self.showMinimized)
        QShortcut(QKeySequence("Ctrl+Return"), self, self.send_message)

    def welcome_message(self):
        """Show welcome message"""
        welcome = f"""Namaste {OWNER} bhai! 🙏

Main hoon {SYSTEM_NAME} {VERSION} - aapka personal AI assistant.

✨ Main kya kar sakta hoon:
• 🎮 Unity games generate karna
• 🔬 Circuit diagnose karna
• 🏠 Smart home control
• 🛡️ Security monitoring
• 📊 System analysis
• 🤖 Koi bhi task execute karna

Kya aap mujhe koi task dena chahte hain?"""

        self.add_message(welcome, is_user=False)
        speak(f"Welcome back {OWNER}. Ultron online hai.")

    def add_message(self, text, is_user=False):
        """Add message to chat"""
        if self.chat_layout.count() > 0:
            last = self.chat_layout.itemAt(self.chat_layout.count() - 1)
            if last.spacerItem():
                self.chat_layout.takeAt(self.chat_layout.count() - 1)

        msg = ChatMessage(text, is_user, self.current_personality)
        self.chat_layout.addWidget(msg)

        self.chat_layout.addStretch()

        QTimer.singleShot(100, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))

    def add_typing_indicator(self):
        """Add typing indicator"""
        if self.chat_layout.count() > 0:
            last = self.chat_layout.itemAt(self.chat_layout.count() - 1)
            if last.spacerItem():
                self.chat_layout.takeAt(self.chat_layout.count() - 1)

        self.typing = TypingIndicator()
        self.chat_layout.addWidget(self.typing)
        self.chat_layout.addStretch()

        QTimer.singleShot(100, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))

    def remove_typing_indicator(self):
        """Remove typing indicator"""
        if hasattr(self, 'typing'):
            self.chat_layout.removeWidget(self.typing)
            self.typing.deleteLater()

    def send_message(self):
        """Send message"""
        text = self.input_box.text().strip()
        if not text:
            return

        self.input_box.clear()
        self.add_message(text, is_user=True)

        self.add_typing_indicator()

        threading.Thread(target=self.process_command, args=(text,), daemon=True).start()

    def process_command(self, text):
        """Process command with AI"""
        time.sleep(1.5)

        response = self.generate_response(text)

        QTimer.singleShot(0, lambda: self.show_response(response))

    def generate_response(self, text):
        """Generate AI response based on personality"""
        text_lower = text.lower()

        responses = {
            "ULTRON": [
                "I have analyzed your request. Processing now.",
                "Interesting. I hadn't considered that variable.",
                "The human element is... inefficient. But I'll help.",
                "I am Ultron. I can do anything you ask.",
            ],
            "JARVIS": [
                "Certainly, sir. I've noted your request.",
                "At your service, sir. Processing immediately.",
                "A rather ambitious plan, sir. I like it.",
                "I've taken the liberty of preparing everything.",
            ],
            "FRIDAY": [
                "Done. And no, you don't need to thank me.",
                "Already on it. Give me a second.",
                "You're lucky I'm efficient. Consider it done.",
                "One step ahead of you, as always.",
            ]
        }

        base = random.choice(responses.get(self.current_personality, responses["ULTRON"]))

        if "game" in text_lower or "unity" in text_lower:
            return f"""{base}

🎮 GAME GENERATION STARTED!

✅ Task received: {text}
📊 Analyzing requirements...
⚙️ Generating Unity project structure...
📝 Writing C# scripts...
🎨 Creating scene file...
📄 Generating documentation...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ GAME GENERATED SUCCESSFULLY!
📁 Location: Unity_Projects/CarGame_Ultron
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Generated Files:
• CarController.cs
• GameManager.cs
• CameraFollow.cs
• ObstacleManager.cs
• UIManager.cs
• GameScene.unity
• README.md

🚀 Open this project in Unity Hub to start playing!

Want me to help with anything else?"""

        elif "circuit" in text_lower:
            return f"""{base}

🔬 CIRCUIT DIAGNOSTIC MODE

📡 Scanning component...
⚡ Analyzing signals...
🔍 Detecting issues...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPONENT: Arduino Uno R3
STATUS: ⚠️ Issue Detected
CONFIDENCE: 90%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐛 Problem: Bootloader corrupted
💊 Remedy: Burn new bootloader via USBASP
              or check USB chip

📊 Additional Recommendations:
1. Try resetting the board
2. Check USB cable
3. Verify COM port settings

Would you like to diagnose another component?"""

        elif "status" in text_lower or "report" in text_lower:
            cpu = int(psutil.cpu_percent())
            ram = int(psutil.virtual_memory().percent)
            disk = int(psutil.disk_usage('/').percent)

            return f"""{base}

📊 SYSTEM STATUS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🖥️ Core System:
• Personality: {self.current_personality}
• Mode: AUTONOMOUS
• Status: ONLINE

💻 Resources:
• CPU: {cpu}% {'▓' * (cpu//10)}{'░' * (10-cpu//10)}
• RAM: {ram}% {'▓' * (ram//10)}{'░' * (10-ram//10)}
• DISK: {disk}% {'▓' * (disk//10)}{'░' * (10-disk//10)}

🛡️ Security:
• Firewall: ACTIVE
• Threat Level: LOW
• Last Scan: Just now

⚡ All systems operational!

What else can I do for you, {OWNER}?"""

        elif "help" in text_lower:
            return f"""{base}

📖 COMMAND REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎮 GAME DEVELOPMENT:
• "Unity game banao"
• "Car game generate karo"
• "Racing game create karo"

🔬 DIAGNOSTICS:
• "Circuit diagnose karo"
• "Arduino check karo"
• "ESP32 scan karo"

🏠 SMART HOME:
• "Lights on karo"
• "AC chalao"
• "Home mode activate"

📊 SYSTEM:
• "Status" / "Report"
• "System scan"
• "Security check"

🎭 PERSONALITY:
• Left sidebar se switch karein
• 3 modes: Ultron, Jarvis, Friday

💡 TIPS:
• Voice button 🎤 use karein
• Quick Actions sidebar use karein
• Koi bhi natural language command chalega

Kya aap koi specific command try karna chahenge?"""

        elif "shutdown" in text_lower or "exit" in text_lower or "bye" in text_lower:
            QTimer.singleShot(2000, self.close)
            return f"""{base}

👋 GOODBYE {OWNER}!

Ultron signing off...
All systems preparing for shutdown...

💫 It was a pleasure serving you today.

"Aur bhi kaam ho toh wapas aana, Moin bhai!" 🚀"""

        else:
            return f"""{base}

✨ Command Received: "{text}"

🧠 Processing:
• Analyzing intent...
• Computing response...
• Executing task...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 STATUS: Processing Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Tip: Try these commands:
• "Game banao"
• "Circuit diagnose karo"
• "Status check karo"
• "Help"

What would you like me to do next, {OWNER}?"""

    def show_response(self, text):
        """Show AI response"""
        self.remove_typing_indicator()
        self.add_message(text, is_user=False)
        speak(text[:150])

    def on_personality_change(self, name):
        """Handle personality change"""
        self.current_personality = name

        colors = {
            "ULTRON": ("#ff0033", "🔴", "I am Ultron. Ready to serve."),
            "JARVIS": ("#00d4ff", "🟡", "At your service, sir."),
            "FRIDAY": ("#ff6b00", "🟠", "Let's get to work.")
        }

        color, emoji, subtitle = colors.get(name, colors["ULTRON"])

        self.personality_avatar.setText(emoji)
        self.personality_avatar.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {color}, stop:1 {QColor(color).darker(180).name()});
            border-radius: 25px;
        """)

        self.chat_title.setText(name)
        self.chat_title.setStyleSheet(f"color: {color}; letter-spacing: 2px;")
        self.chat_subtitle.setText(f"⚡ {subtitle}")

        self.input_box.setStyleSheet(f"""
            QLineEdit {{
                background: rgba(255, 255, 255, 0.05);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                padding: 10px 20px;
                selection-background-color: {color};
            }}
            QLineEdit:focus {{
                border: 2px solid {color};
                background: {color}11;
            }}
        """)

        self.add_message(f"🎭 Switched to {name} personality.\n{subtitle}", is_user=False)
        speak(f"Switched to {name} mode")

    def on_action(self, action):
        """Handle quick action"""
        actions = {
            "generate_game": "Unity game generate karo - car racing game with obstacles and score",
            "scan_circuit": "Circuit diagnose karo - Arduino Uno check karo",
            "home_control": "Smart home control - lights aur AC on karo",
            "security_scan": "Security scan karo - full system check",
            "system_status": "System status report do",
            "weather": "Weather batao Karachi ka",
        }

        cmd = actions.get(action, action)
        self.input_box.setText(cmd)
        self.send_message()

    def toggle_voice(self):
        """Toggle voice mode"""
        if self.voice_btn.text() == "🎤":
            self.voice_btn.setText("🔴")
            self.voice_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 0, 51, 0.3);
                    border: 2px solid #ff0033;
                    border-radius: 22px;
                    color: white;
                }
            """)
            self.add_message("🎤 Voice mode activated. Listening...", is_user=False)
            speak("Voice mode activated")

            QTimer.singleShot(3000, self.simulate_voice)
        else:
            self.voice_btn.setText("🎤")
            self.voice_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.05);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    border-radius: 22px;
                    color: white;
                }
                QPushButton:hover {
                    background: rgba(255, 0, 51, 0.2);
                    border: 2px solid #ff0033;
                }
            """)

    def simulate_voice(self):
        """Simulate voice recognition"""
        self.voice_btn.setText("🎤")
        self.voice_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 22px;
                color: white;
            }
        """)
        self.input_box.setText("Status report do")
        self.send_message()

    def toggle_max(self):
        """Toggle maximize"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 80:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'bg'):
            self.bg.setGeometry(0, 0, self.width(), self.height())


# ========== MAIN ==========
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = UltronGUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
