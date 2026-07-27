import io
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def generate_category_chart(category_totals):
    if not category_totals:
        return None

    labels = [row["category"] for row in category_totals]
    values = [row["total"] for row in category_totals]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    ax.set_title("Spending by Category")

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)

    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    return encoded