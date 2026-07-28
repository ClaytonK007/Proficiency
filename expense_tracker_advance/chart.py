import io
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def fig_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def generate_category_chart(category_totals, chart_type="pie"):
    if not category_totals:
        return None

    labels = [row["category"] for row in category_totals]
    values = [row["total"] for row in category_totals]

    fig, ax = plt.subplots(figsize=(6, 6))

    if chart_type == "bar":
        ax.bar(labels, values, color="#4a90d9")
        ax.set_ylabel("Amount (R)")
        ax.set_title("Spending by Category")
        plt.xticks(rotation=30, ha="right")
    else:
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        ax.set_title("Spending by Category")

    return fig_to_base64(fig)

def generate_monthly_trend_chart(monthly_totals):
    if not monthly_totals:
        return None

    months = [row["month"] for row in monthly_totals]
    totals = [row["total"] for row in monthly_totals]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(months, totals, marker="o", color="#4a90d9")
    ax.set_ylabel("Amount (R)")
    ax.set_title("Monthly Spending Trend")
    plt.xticks(rotation=30, ha="right")

    return fig_to_base64(fig)