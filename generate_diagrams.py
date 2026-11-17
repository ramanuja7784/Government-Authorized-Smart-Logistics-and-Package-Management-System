import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

OUTPUT_DIR = r"d:\final year project\.images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name + ".png")
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {path}")

# ─────────────────────────────────────────────
# 1. USE CASE DIAGRAM
# ─────────────────────────────────────────────
def draw_use_case():
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    ax.set_title("Use Case Diagram – GA-SLMP System", fontsize=16, fontweight='bold', pad=20)

    # System boundary
    rect = FancyBboxPatch((3.5, 0.5), 9, 10, boxstyle="round,pad=0.1",
                           linewidth=2, edgecolor='#2c3e50', facecolor='#ecf0f1')
    ax.add_patch(rect)
    ax.text(8, 10.3, "GA-SLMP System", ha='center', fontsize=12, fontweight='bold', color='#2c3e50')

    def actor(x, y, name):
        # head
        circle = plt.Circle((x, y+0.5), 0.25, color='#2c3e50', zorder=5)
        ax.add_patch(circle)
        # body
        ax.plot([x, x], [y+0.25, y-0.3], color='#2c3e50', lw=2)
        # arms
        ax.plot([x-0.35, x+0.35], [y+0.05, y+0.05], color='#2c3e50', lw=2)
        # legs
        ax.plot([x, x-0.3], [y-0.3, y-0.7], color='#2c3e50', lw=2)
        ax.plot([x, x+0.3], [y-0.3, y-0.7], color='#2c3e50', lw=2)
        ax.text(x, y-1.0, name, ha='center', fontsize=9, fontweight='bold', color='#2c3e50')

    def use_case(x, y, label, color='#3498db'):
        ellipse = mpatches.Ellipse((x, y), 2.2, 0.7, color=color, zorder=4, alpha=0.85)
        ax.add_patch(ellipse)
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5, color='white', fontweight='bold', zorder=5)

    def line(ax, x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-", color='#555555', lw=1.2))

    # Actors
    actor(1.5, 8.5, "Courier\n(Admin)")
    actor(1.5, 5.5, "Delivery\nBoy")
    actor(14.5, 6.5, "Government\nAuthority")

    # Use cases – Courier
    uc_data = [
        (6.5, 9.5, "Register / Login"),
        (6.5, 8.5, "Create Shipment"),
        (6.5, 7.5, "View All Shipments"),
        (6.5, 6.5, "Assign Delivery Boy"),
        (6.5, 5.5, "View Risk Score"),
        (10.5, 9.5, "View Assigned Shipments"),
        (10.5, 8.5, "Update Delivery Status"),
        (10.5, 7.5, "View Addresses"),
        (10.5, 6.5, "View Pending Approvals"),
        (10.5, 5.5, "Approve / Flag Shipment"),
        (8.5, 4.5, "Receive Notifications"),
        (8.5, 3.5, "View Reports Dashboard"),
    ]
    for x, y, label in uc_data:
        use_case(x, y, label)

    # Courier lines
    for uc_x, uc_y, _ in uc_data[:5]:
        line(ax, 1.5, 8.5, uc_x - 1.1, uc_y)
    line(ax, 1.5, 8.5, 7.4, 4.5)
    line(ax, 1.5, 8.5, 7.4, 3.5)

    # Delivery Boy lines
    for uc_x, uc_y, _ in uc_data[5:9]:
        line(ax, 1.5, 5.5, uc_x - 1.1, uc_y)
    line(ax, 1.5, 5.5, 7.4, 4.5)

    # Gov Auth lines
    for uc_x, uc_y, _ in uc_data[8:12]:
        line(ax, 14.5, 6.5, uc_x + 1.1, uc_y)

    save(fig, "01_use_case_diagram")

# ─────────────────────────────────────────────
# 2. CLASS DIAGRAM
# ─────────────────────────────────────────────
def draw_class():
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_title("Class Diagram – GA-SLMP System", fontsize=16, fontweight='bold', pad=15)

    def class_box(ax, x, y, w, h, title, attrs, methods, color='#3498db'):
        title_h = 0.6
        attr_h = len(attrs) * 0.35
        meth_h = len(methods) * 0.35
        total_h = title_h + attr_h + meth_h + 0.4

        # Border
        rect = FancyBboxPatch((x, y - total_h), w, total_h, boxstyle="square,pad=0",
                               linewidth=1.5, edgecolor='#2c3e50', facecolor='white')
        ax.add_patch(rect)
        # Title bar
        title_rect = FancyBboxPatch((x, y - title_h), w, title_h, boxstyle="square,pad=0",
                                     linewidth=0, edgecolor='none', facecolor=color)
        ax.add_patch(title_rect)
        ax.text(x + w / 2, y - title_h / 2, title, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')

        # Divider 1
        div1 = y - title_h
        ax.plot([x, x + w], [div1, div1], color='#2c3e50', lw=1)

        # Attributes
        for i, attr in enumerate(attrs):
            ax.text(x + 0.1, div1 - 0.2 - i * 0.35, attr, fontsize=7.5, va='top', color='#2c3e50')

        # Divider 2
        div2 = div1 - attr_h - 0.1
        ax.plot([x, x + w], [div2, div2], color='#2c3e50', lw=1)

        # Methods
        for i, meth in enumerate(methods):
            ax.text(x + 0.1, div2 - 0.2 - i * 0.35, meth, fontsize=7.5, va='top',
                    color='#8e44ad', fontstyle='italic')

        return (x + w / 2, y - total_h / 2, total_h)

    classes = [
        (1, 11.5, 4, "User", ["+id: int", "+username: String", "+password: String", "+email: String"],
         ["+login(): void", "+logout(): void"], '#2980b9'),
        (7, 11.5, 4.5, "UserProfile", ["+id: int", "+role: String"],
         ["+getRole(): String"], '#27ae60'),
        (1, 6.5, 4.5, "Shipment",
         ["+id: int", "+senderName: String", "+receiverName: String",
          "+packageType: String", "+weight: float", "+riskScore: String",
          "+status: String", "+isApproved: bool"],
         ["+calculateRiskScore(): String", "+updateStatus(): void"], '#e67e22'),
        (7, 7, 4.5, "Notification",
         ["+id: int", "+message: String", "+isRead: bool", "+createdAt: DateTime"],
         ["+markAsRead(): void"], '#8e44ad'),
        (13, 9, 4.5, "ComplianceAction",
         ["+id: int", "+action: String", "+actionDate: DateTime"],
         ["+approve(): void", "+flag(): void"], '#c0392b'),
    ]

    centers = {}
    for x, y, w, name, attrs, methods, color in classes:
        cx = x + w / 2
        title_h = 0.6
        attr_h = len(attrs) * 0.35
        meth_h = len(methods) * 0.35
        total_h = title_h + attr_h + meth_h + 0.4
        cy = y - total_h / 2
        centers[name] = (cx, y, y - total_h)
        class_box(ax, x, y, w, total_h, name, attrs, methods, color)

    def rel_line(ax, name1, name2, label='', mult1='', mult2='', color='#555'):
        c1 = centers[name1]
        c2 = centers[name2]
        x1, y1 = c1[0], (c1[1] + c1[2]) / 2
        x2, y2 = c2[0], (c2[1] + c2[2]) / 2
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if label:
            ax.text(mx, my + 0.15, label, ha='center', fontsize=8, color='#2c3e50', fontweight='bold')
        if mult1:
            ax.text(x1 + 0.2, y1 + 0.2, mult1, fontsize=8, color='#c0392b')
        if mult2:
            ax.text(x2 - 0.2, y2 + 0.2, mult2, fontsize=8, color='#c0392b')

    rel_line(ax, 'User', 'UserProfile', 'has', '1', '1')
    rel_line(ax, 'User', 'Shipment', 'creates', '1', '0..*')
    rel_line(ax, 'User', 'Notification', 'receives', '1', '0..*')
    rel_line(ax, 'Shipment', 'ComplianceAction', 'reviewed by', '1', '0..*')

    save(fig, "02_class_diagram")

# ─────────────────────────────────────────────
# 3. SEQUENCE DIAGRAM
# ─────────────────────────────────────────────
def draw_sequence():
    fig, ax = plt.subplots(figsize=(18, 13))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 13)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_title("Sequence Diagram – High-Risk Shipment Creation & Approval", fontsize=14, fontweight='bold', pad=15)

    lifelines = ["Courier", "Browser", "Django\nView", "Risk\nEngine", "Database", "Notif\nSystem", "Gov\nAuthority"]
    x_pos = [1.2, 3.5, 6, 8.5, 11, 13.5, 16.5]
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']

    top = 12.5
    for i, (name, x, color) in enumerate(zip(lifelines, x_pos, colors)):
        r = FancyBboxPatch((x - 0.7, top - 0.4), 1.4, 0.8, boxstyle="round,pad=0.05",
                           linewidth=1.5, edgecolor=color, facecolor=color)
        ax.add_patch(r)
        ax.text(x, top, name, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
        ax.plot([x, x], [top - 0.4, 0.3], color='#aaa', lw=1, linestyle='--')

    def msg(ax, x1, x2, y, label, ret=False):
        style = "<|-" if ret else "-|>"
        color = '#888' if ret else '#2c3e50'
        ls = '--' if ret else '-'
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.3, linestyle=ls))
        mx = (x1 + x2) / 2
        ax.text(mx, y + 0.12, label, ha='center', fontsize=7.2, color='#2c3e50', fontweight='bold')

    steps = [
        (0, 1, 11.8, "1. Fill Shipment Form & Submit", False),
        (1, 2, 11.1, "2. POST /shipments/create/", False),
        (2, 4, 10.4, "3. Save Shipment Record", False),
        (2, 3, 9.7, "4. calculate_risk_score()", False),
        (3, 2, 9.0, "5. Returns 'HIGH'", True),
        (2, 4, 8.3, "6. Update risk_score=HIGH, is_approved=False", False),
        (2, 5, 7.6, "7. Trigger Notification", False),
        (5, 4, 6.9, "8. Save Notification Record", False),
        (2, 1, 6.2, "9. Redirect to Shipment List", True),
        (4, 6, 5.5, "10. Bell Icon – Unread Notification", False),
        (6, 2, 4.8, "11. POST /compliance/approve/<id>/", False),
        (2, 4, 4.1, "12. Update is_approved=True", False),
        (2, 5, 3.4, "13. Notify Courier", False),
        (2, 6, 2.7, "14. Redirect to Compliance Dashboard", True),
    ]

    for x1i, x2i, y, label, ret in steps:
        msg(ax, x_pos[x1i], x_pos[x2i], y, label, ret)

    save(fig, "03_sequence_diagram")

# ─────────────────────────────────────────────
# 4. ACTIVITY DIAGRAM
# ─────────────────────────────────────────────
def draw_activity():
    fig, ax = plt.subplots(figsize=(13, 17))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 17)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_title("Activity Diagram – Shipment Workflow", fontsize=15, fontweight='bold', pad=15)

    def activity(x, y, text, w=3.5, h=0.55, color='#3498db'):
        r = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1",
                           linewidth=1.5, edgecolor='#2c3e50', facecolor=color)
        ax.add_patch(r)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, color='white', fontweight='bold')

    def decision(x, y, text):
        d = plt.Polygon([[x, y+0.5], [x+1.1, y], [x, y-0.5], [x-1.1, y]],
                        closed=True, linewidth=1.5, edgecolor='#2c3e50', facecolor='#f39c12')
        ax.add_patch(d)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    def arrow(ax, x1, y1, x2, y2, label=''):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color='#2c3e50', lw=1.5))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx+0.15, my, label, fontsize=8, color='#c0392b', fontweight='bold')

    # Start
    circle = plt.Circle((6.5, 16.5), 0.3, color='#2c3e50', zorder=5)
    ax.add_patch(circle)

    activity(6.5, 15.7, "Courier Logs In", color='#2980b9')
    activity(6.5, 14.8, "Navigate to Create Shipment", color='#2980b9')
    activity(6.5, 13.9, "Fill Shipment Form", color='#2980b9')
    activity(6.5, 13.0, "Submit Form", color='#2980b9')
    decision(6.5, 12.0, "Form Valid?")
    activity(6.5, 11.0, "Save Shipment to Database", color='#27ae60')
    activity(6.5, 10.1, "Calculate Risk Score", color='#27ae60')
    decision(6.5, 9.0, "Risk Level?")

    # Low/Medium path (left)
    activity(2.5, 8.0, "Mark Shipment Safe", color='#27ae60')
    activity(2.5, 7.1, "Assign to Delivery Boy", color='#27ae60')
    activity(2.5, 6.2, "Delivery Boy Views Assignment", color='#2980b9')
    activity(2.5, 5.3, "Update Delivery Status", color='#2980b9')

    # High path (right)
    activity(10.5, 8.0, "Quarantine – Pending Approval", color='#e74c3c')
    activity(10.5, 7.1, "Notify Government Authority", color='#e74c3c')
    activity(10.5, 6.2, "Authority Reviews Shipment", color='#e74c3c')
    decision(10.5, 5.2, "Decision?")
    activity(10.5, 4.1, "Block Shipment – Notify Courier", color='#c0392b')

    # End nodes
    end1 = plt.Circle((2.5, 4.4), 0.3, color='white', ec='#2c3e50', lw=2, zorder=4)
    end1_inner = plt.Circle((2.5, 4.4), 0.18, color='#2c3e50', zorder=5)
    end2 = plt.Circle((10.5, 3.2), 0.3, color='white', ec='#2c3e50', lw=2, zorder=4)
    end2_inner = plt.Circle((10.5, 3.2), 0.18, color='#2c3e50', zorder=5)
    for p in [end1, end1_inner, end2, end2_inner]:
        ax.add_patch(p)

    # Arrows
    arrow(ax, 6.5, 16.2, 6.5, 16.0)
    arrow(ax, 6.5, 15.45, 6.5, 15.05)
    arrow(ax, 6.5, 14.55, 6.5, 14.15)
    arrow(ax, 6.5, 13.65, 6.5, 13.25)
    arrow(ax, 6.5, 12.75, 6.5, 12.5)
    # Form valid - No
    ax.annotate("", xy=(4.5, 13.9), xytext=(5.4, 12.0),
                arrowprops=dict(arrowstyle="-|>", color='#e74c3c', lw=1.5,
                                connectionstyle="arc3,rad=0.3"))
    ax.text(4.2, 13.0, "No", fontsize=8, color='#e74c3c', fontweight='bold')
    # Form valid - Yes
    arrow(ax, 6.5, 11.5, 6.5, 11.25, "Yes")
    arrow(ax, 6.5, 10.75, 6.5, 10.35)
    arrow(ax, 6.5, 9.75, 6.5, 9.5)
    # Risk - Low/Medium
    arrow(ax, 5.4, 9.0, 2.5, 8.25, "Low/Med")
    arrow(ax, 2.5, 7.75, 2.5, 7.4)
    arrow(ax, 2.5, 6.85, 2.5, 6.5)
    arrow(ax, 2.5, 5.95, 2.5, 5.6)
    arrow(ax, 2.5, 5.05, 2.5, 4.7)
    # Risk - High
    arrow(ax, 7.6, 9.0, 10.5, 8.25, "High")
    arrow(ax, 10.5, 7.75, 10.5, 7.4)
    arrow(ax, 10.5, 6.85, 10.5, 6.5)
    arrow(ax, 10.5, 5.95, 10.5, 5.7)
    # Decision - Approve
    ax.annotate("", xy=(2.5, 7.1), xytext=(9.4, 5.2),
                arrowprops=dict(arrowstyle="-|>", color='#27ae60', lw=1.5,
                                connectionstyle="arc3,rad=-0.3"))
    ax.text(6.0, 4.5, "Approve", fontsize=8, color='#27ae60', fontweight='bold')
    # Decision - Flag
    arrow(ax, 10.5, 4.7, 10.5, 4.4, "Flag")
    arrow(ax, 10.5, 3.75, 10.5, 3.5)

    save(fig, "04_activity_diagram")

# ─────────────────────────────────────────────
# 5. COLLABORATION DIAGRAM
# ─────────────────────────────────────────────
def draw_collaboration():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_title("Collaboration Diagram – Shipment Approval", fontsize=15, fontweight='bold', pad=15)

    objects = {
        "courier:Courier":      (2.0, 8.0),
        "shipment:Shipment":    (7.0, 8.0),
        "riskEngine:RiskEngine":(11.5, 5.5),
        "notification:Notification": (7.0, 2.5),
        "govAuthority:GovAuthority": (2.0, 5.0),
    }
    colors = ['#2980b9', '#e67e22', '#e74c3c', '#8e44ad', '#27ae60']

    for (name, (x, y)), color in zip(objects.items(), colors):
        r = FancyBboxPatch((x - 1.4, y - 0.35), 2.8, 0.7, boxstyle="round,pad=0.05",
                           linewidth=2, edgecolor=color, facecolor=color)
        ax.add_patch(r)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    msgs = [
        ("courier:Courier", "shipment:Shipment", "1: create(shipment_data)"),
        ("shipment:Shipment", "riskEngine:RiskEngine", "2: calculate_risk_score()"),
        ("riskEngine:RiskEngine", "shipment:Shipment", "3: return risk_level=HIGH"),
        ("shipment:Shipment", "notification:Notification", "4: create_notification(gov)"),
        ("notification:Notification", "govAuthority:GovAuthority", "5: deliver_alert()"),
        ("govAuthority:GovAuthority", "shipment:Shipment", "6: approve() / flag()"),
        ("shipment:Shipment", "notification:Notification", "7: create_notification(courier)"),
        ("notification:Notification", "courier:Courier", "8: deliver_alert()"),
    ]
    colors_msg = ['#2c3e50']*8

    for (src, dst, label), color in zip(msgs, colors_msg):
        x1, y1 = objects[src]
        x2, y2 = objects[dst]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4,
                                   connectionstyle="arc3,rad=0.1"))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.22, label, ha='center', fontsize=8, color='#2c3e50',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#fffde7', edgecolor='#f0c040', alpha=0.85))

    save(fig, "05_collaboration_diagram")

# ─────────────────────────────────────────────
# 6. DEPLOYMENT DIAGRAM
# ─────────────────────────────────────────────
def draw_deployment():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_title("Deployment Diagram – GA-SLMP System", fontsize=15, fontweight='bold', pad=15)

    def node(ax, x, y, w, h, title, components, color='#2980b9'):
        # 3D effect
        offset = 0.3
        face3d = mpatches.FancyBboxPatch((x+offset, y+offset), w, h, boxstyle="square,pad=0",
                                          facecolor='#bdc3c7', edgecolor='#7f8c8d', lw=1)
        ax.add_patch(face3d)
        main = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                        facecolor='#ecf0f1', edgecolor='#2c3e50', lw=2)
        ax.add_patch(main)
        # Title bar
        tbar = mpatches.FancyBboxPatch((x, y+h-0.55), w, 0.55, boxstyle="square,pad=0",
                                        facecolor=color, edgecolor='none', lw=0)
        ax.add_patch(tbar)
        ax.text(x+w/2, y+h-0.27, f"<<device>>\n{title}", ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')
        for i, comp in enumerate(components):
            cy = y + h - 0.8 - i * 0.65
            cr = mpatches.FancyBboxPatch((x+0.2, cy-0.22), w-0.4, 0.44, boxstyle="round,pad=0.05",
                                          facecolor='white', edgecolor=color, lw=1.5)
            ax.add_patch(cr)
            ax.text(x+w/2, cy, comp, ha='center', va='center', fontsize=8, color='#2c3e50')

    node(ax, 0.5, 5.5, 3.5, 2.5, "Client Machine",
         ["Web Browser", "(Chrome / Firefox / Edge)"], '#3498db')

    node(ax, 5.0, 3.5, 4.5, 4.5, "Application Server",
         ["Django App (Python 3.11+)", "Gunicorn WSGI Server", "Static Files (CSS/JS)"], '#e67e22')

    node(ax, 10.5, 5.0, 3.0, 3.0, "Database Server",
         ["MySQL Database\n(Production)"], '#e74c3c')

    # Connection lines
    ax.annotate("", xy=(5.0, 6.5), xytext=(4.0, 6.5),
                arrowprops=dict(arrowstyle="<->", color='#2c3e50', lw=2))
    ax.text(4.5, 6.75, "HTTP/HTTPS\n:80 / :443", ha='center', fontsize=8, color='#2c3e50', fontweight='bold')

    ax.annotate("", xy=(10.5, 6.0), xytext=(9.5, 6.0),
                arrowprops=dict(arrowstyle="<->", color='#2c3e50', lw=2))
    ax.text(10.0, 6.3, "Django ORM\nTCP :3306", ha='center', fontsize=8, color='#2c3e50', fontweight='bold')

    save(fig, "06_deployment_diagram")

# ─────────────────────────────────────────────
# 7. COMPONENT DIAGRAM
# ─────────────────────────────────────────────
def draw_component():
    fig, ax = plt.subplots(figsize=(15, 11))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 11)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_title("Component Diagram – GA-SLMP System", fontsize=15, fontweight='bold', pad=15)

    def layer_box(ax, y_start, height, label, color):
        r = FancyBboxPatch((0.3, y_start), 14.4, height, boxstyle="round,pad=0.1",
                           linewidth=2, edgecolor=color, facecolor=color+'18')
        ax.add_patch(r)
        ax.text(0.6, y_start + height/2, label, fontsize=9, fontweight='bold',
                color=color, rotation=90, va='center')

    def component(ax, x, y, label, color='#3498db'):
        w, h = 2.6, 0.65
        r = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.08",
                           linewidth=1.5, edgecolor=color, facecolor='white')
        ax.add_patch(r)
        # UML component notch
        for nx, ny in [(x+w/2-0.15, y+0.12), (x+w/2-0.15, y-0.12)]:
            nr = FancyBboxPatch((nx, ny-0.08), 0.25, 0.16, boxstyle="square,pad=0",
                                linewidth=1, edgecolor=color, facecolor='white')
            ax.add_patch(nr)
        ax.text(x-0.1, y, label, ha='center', va='center', fontsize=8, color='#2c3e50', fontweight='bold')
        return (x, y)

    layer_box(ax, 8.5, 2.0, "Client Layer", '#3498db')
    layer_box(ax, 3.8, 4.5, "Application Layer (Django)", '#e67e22')
    layer_box(ax, 0.5, 3.0, "Data Layer", '#27ae60')

    # Client
    ui = component(ax, 7.5, 9.5, "Web UI Templates\nHTML / CSS / JS", '#3498db')

    # App layer
    router = component(ax, 7.5, 7.8, "URL Router\nurls.py", '#e67e22')
    acc = component(ax, 2.2, 6.7, "Accounts Module\n(Auth, RBAC)", '#e67e22')
    ship = component(ax, 5.0, 6.7, "Shipments Module\n(Risk Engine)", '#e67e22')
    comp = component(ax, 7.8, 6.7, "Compliance Module\n(Approvals)", '#e67e22')
    deliv = component(ax, 10.6, 6.7, "Delivery Module\n(Operations)", '#e67e22')
    rep = component(ax, 13.2, 6.7, "Reports Module\n(Analytics)", '#e67e22')
    ctx = component(ax, 4.5, 5.5, "Context Processor\n(Global Notifications)", '#e67e22')

    # Data layer
    orm = component(ax, 5.5, 2.2, "Django ORM", '#27ae60')
    db_r = FancyBboxPatch((9.5, 1.5), 3.0, 1.4, boxstyle="round,pad=0.1",
                          linewidth=1.5, edgecolor='#27ae60', facecolor='white')
    ax.add_patch(db_r)
    ax.text(11.0, 2.2, "MySQL / SQLite\nDatabase", ha='center', va='center',
            fontsize=8.5, color='#2c3e50', fontweight='bold')

    def dep_arrow(ax, p1, p2):
        ax.annotate("", xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="-|>", color='#7f8c8d', lw=1.2, linestyle='dashed'))

    dep_arrow(ax, ui, router)
    for mod in [acc, ship, comp, deliv, rep]:
        dep_arrow(ax, router, mod)
    dep_arrow(ax, acc, ctx)
    dep_arrow(ax, ctx, ui)
    for mod in [acc, ship, comp, deliv, rep]:
        dep_arrow(ax, mod, orm)
    dep_arrow(ax, orm, (11.0, 2.9))

    save(fig, "07_component_diagram")

# ─────────────────────────────────────────────
# 8. ER DIAGRAM
# ─────────────────────────────────────────────
def draw_er():
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_title("Entity Relationship (ER) Diagram – GA-SLMP Database", fontsize=15, fontweight='bold', pad=15)

    def entity(ax, x, y, name, color='#2980b9'):
        r = FancyBboxPatch((x-1.2, y-0.35), 2.4, 0.7, boxstyle="square,pad=0",
                           linewidth=2, edgecolor='#2c3e50', facecolor=color)
        ax.add_patch(r)
        ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold', color='white')

    def attr_oval(ax, x, y, text, pk=False):
        style = 'bold' if pk else 'normal'
        e = mpatches.Ellipse((x, y), 1.8, 0.5, linewidth=1.3,
                              edgecolor='#2c3e50', facecolor='#d6eaf8')
        ax.add_patch(e)
        label = f"[PK] {text}" if pk else text
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5,
                fontweight=style, color='#2c3e50')

    def rel_diamond(ax, x, y, text):
        d = plt.Polygon([[x, y+0.45], [x+1.0, y], [x, y-0.45], [x-1.0, y]],
                        closed=True, linewidth=1.5, edgecolor='#2c3e50', facecolor='#f9e79f')
        ax.add_patch(d)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#2c3e50')

    def connect(ax, x1, y1, x2, y2, label=''):
        ax.plot([x1, x2], [y1, y2], color='#555', lw=1.3)
        if label:
            ax.text((x1+x2)/2+0.1, (y1+y2)/2+0.1, label, fontsize=8, color='#c0392b', fontweight='bold')

    # Entities
    entity(ax, 4.0, 10.5, "USER", '#2980b9')
    entity(ax, 10.0, 10.5, "USERPROFILE", '#27ae60')
    entity(ax, 4.0, 6.5, "SHIPMENT", '#e67e22')
    entity(ax, 4.0, 2.5, "NOTIFICATION", '#8e44ad')
    entity(ax, 13.0, 6.5, "COMPLIANCEACTION", '#c0392b')

    # USER attrs
    for ax_off, ay_off, txt, pk in [
        (-2.5, 10.8, "id", True), (-2.5, 10.5, "username", False),
        (-2.5, 10.2, "password", False), (-2.5, 9.9, "email", False)]:
        attr_oval(ax, 4.0+ax_off, 10.5+ay_off-10.5+ay_off, txt, pk)

    # Simple attribute listing near entities
    for i, (txt, pk) in enumerate([("id (PK)", True), ("username", False), ("password", False), ("email", False)]):
        attr_oval(ax, 1.5, 10.8 - i*0.6, txt, pk)
        connect(ax, 2.4, 10.8 - i*0.6, 2.8, 10.5)

    for i, (txt, pk) in enumerate([("id (PK)", True), ("role", False)]):
        attr_oval(ax, 12.5, 10.8 - i*0.6, txt, pk)
        connect(ax, 11.6, 10.8 - i*0.6, 11.2, 10.5)

    for i, (txt, pk) in enumerate([("id (PK)", True), ("sender_name", False), ("receiver_name", False),
                                    ("package_type", False), ("risk_score", False), ("is_approved", False)]):
        attr_oval(ax, 1.5, 7.2 - i*0.6, txt, pk)
        connect(ax, 2.4, 7.2 - i*0.6, 2.8, 6.5)

    for i, (txt, pk) in enumerate([("id (PK)", True), ("message", False), ("is_read", False), ("created_at", False)]):
        attr_oval(ax, 1.5, 3.2 - i*0.6, txt, pk)
        connect(ax, 2.4, 3.2 - i*0.6, 2.8, 2.5)

    for i, (txt, pk) in enumerate([("id (PK)", True), ("action", False), ("action_date", False)]):
        attr_oval(ax, 16.0, 7.2 - i*0.6, txt, pk)
        connect(ax, 15.1, 7.2 - i*0.6, 14.5, 6.5)

    # Relationships
    rel_diamond(ax, 7.0, 10.5, "has")
    connect(ax, 5.2, 10.5, 6.0, 10.5, "1")
    connect(ax, 8.0, 10.5, 8.8, 10.5, "1")

    rel_diamond(ax, 4.0, 8.8, "creates")
    connect(ax, 4.0, 10.15, 4.0, 9.25, "1")
    connect(ax, 4.0, 8.35, 4.0, 6.85, "N")

    rel_diamond(ax, 4.0, 4.8, "receives")
    connect(ax, 4.0, 6.15, 4.0, 5.25, "1")
    connect(ax, 4.0, 4.35, 4.0, 2.85, "N")

    rel_diamond(ax, 8.5, 6.5, "reviewed in")
    connect(ax, 5.2, 6.5, 7.5, 6.5, "1")
    connect(ax, 9.5, 6.5, 11.8, 6.5, "N")

    save(fig, "08_er_diagram")

# ─────────────────────────────────────────────
# 9. DFD DIAGRAM
# ─────────────────────────────────────────────
def draw_dfd():
    fig, ax = plt.subplots(figsize=(16, 14))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_title("Data Flow Diagram (DFD) – GA-SLMP System", fontsize=15, fontweight='bold', pad=15)

    # --- Level 0 ---
    ax.text(8, 13.6, "Level 0 – Context Diagram", ha='center', fontsize=12, fontweight='bold', color='#2c3e50')
    ax.add_patch(plt.Circle((8, 11.5), 1.0, color='#3498db', alpha=0.85, zorder=4))
    ax.text(8, 11.5, "0\nGA-SLMP\nSystem", ha='center', va='center', fontsize=8.5,
            fontweight='bold', color='white', zorder=5)

    def ext_entity(x, y, label):
        r = FancyBboxPatch((x-1.1, y-0.35), 2.2, 0.7, boxstyle="square,pad=0",
                           linewidth=2, edgecolor='#2c3e50', facecolor='#ecf0f1')
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='#2c3e50')

    def dfd_arrow(ax, x1, y1, x2, y2, label, offset=0.15):
        ax.annotate("", xy=(x2+(x2-x1)*0.01, y2+(y2-y1)*0.01),
                    xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color='#2c3e50', lw=1.5))
        ax.text((x1+x2)/2, (y1+y2)/2 + offset, label, ha='center', fontsize=8,
                color='#c0392b', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.7))

    ext_entity(2.5, 11.5, "Courier")
    ext_entity(8.0, 13.2, "Delivery Boy")
    ext_entity(13.5, 11.5, "Gov Authority")

    dfd_arrow(ax, 3.6, 11.7, 7.0, 11.7, "Shipment Data")
    dfd_arrow(ax, 7.0, 11.3, 3.6, 11.3, "Notifications/Confirmations")
    dfd_arrow(ax, 8.0, 12.5, 8.2, 12.5, "Status Updates")
    dfd_arrow(ax, 8.4, 12.3, 8.2, 12.1, "Assigned Deliveries")
    dfd_arrow(ax, 12.4, 11.7, 9.0, 11.7, "Approval Decisions")
    dfd_arrow(ax, 9.0, 11.3, 12.4, 11.3, "Pending Approvals/Reports")

    # --- Level 1 ---
    ax.plot([0.3, 15.7], [9.8, 9.8], color='#aaa', lw=1, linestyle='--')
    ax.text(8, 9.5, "Level 1 – Internal Data Flow", ha='center', fontsize=12,
            fontweight='bold', color='#2c3e50')

    processes = {
        "P1\nAuth": (2.5, 8.2),
        "P2\nCreate\nShipment": (5.5, 8.2),
        "P3\nRisk\nScore": (8.5, 8.2),
        "P4\nCompliance": (11.5, 8.2),
        "P5\nDelivery": (8.5, 5.5),
        "P6\nNotify": (5.5, 5.5),
    }
    colors_p = ['#3498db', '#e67e22', '#e74c3c', '#f39c12', '#27ae60', '#8e44ad']
    proc_centers = {}
    for (name, (x, y)), color in zip(processes.items(), colors_p):
        circle = plt.Circle((x, y), 0.75, color=color, alpha=0.85, zorder=4)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color='white', zorder=5)
        proc_centers[name] = (x, y)

    def data_store(ax, x, y, label, color='#2c3e50'):
        ax.plot([x-1.1, x+1.1], [y+0.25, y+0.25], color=color, lw=2)
        ax.plot([x-1.1, x+1.1], [y-0.25, y-0.25], color=color, lw=2)
        ax.plot([x-1.1, x-1.1], [y-0.25, y+0.25], color=color, lw=2)
        ax.text(x, y, label, ha='center', va='center', fontsize=8.5,
                fontweight='bold', color=color)

    data_store(ax, 2.5, 6.8, "D1: User Store", '#2980b9')
    data_store(ax, 8.5, 3.5, "D2: Shipment Store", '#e67e22')
    data_store(ax, 14.0, 5.5, "D3: Notification Store", '#8e44ad')

    def p_arrow(ax, n1, n2, label=''):
        x1, y1 = proc_centers[n1]
        x2, y2 = proc_centers[n2]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color='#555', lw=1.2))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2+0.15, label, ha='center', fontsize=7.5,
                    color='#c0392b',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.7))

    p_arrow(ax, "P1\nAuth", "P2\nCreate\nShipment", "auth user")
    p_arrow(ax, "P2\nCreate\nShipment", "P3\nRisk\nScore", "shipment")
    p_arrow(ax, "P3\nRisk\nScore", "P4\nCompliance", "high risk")
    p_arrow(ax, "P4\nCompliance", "P6\nNotify", "decision")
    p_arrow(ax, "P3\nRisk\nScore", "P5\nDelivery", "safe shipment")

    ax.annotate("", xy=(2.5, 7.05), xytext=(2.5, 7.45),
                arrowprops=dict(arrowstyle="-|>", color='#555', lw=1.2))
    ax.text(3.2, 7.2, "store", fontsize=7.5, color='#555')

    ax.annotate("", xy=(8.5, 4.25), xytext=(8.5, 7.45),
                arrowprops=dict(arrowstyle="-|>", color='#555', lw=1.2))
    ax.text(9.0, 5.8, "save", fontsize=7.5, color='#555')

    ax.annotate("", xy=(13.0, 5.5), xytext=(6.25, 5.5),
                arrowprops=dict(arrowstyle="-|>", color='#555', lw=1.2))
    ax.text(9.5, 5.7, "notify", fontsize=7.5, color='#555')

    save(fig, "09_dfd_diagram")


if __name__ == "__main__":
    print("Generating GA-SLMP diagrams...")
    draw_use_case()
    draw_class()
    draw_sequence()
    draw_activity()
    draw_collaboration()
    draw_deployment()
    draw_component()
    draw_er()
    draw_dfd()
    print(f"\nAll diagrams saved to: {OUTPUT_DIR}")
