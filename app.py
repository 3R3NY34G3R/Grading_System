import streamlit as st

st.set_page_config(page_title="Grade Calculator", layout="centered")
st.title("Student Grade Calculator")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
for key in ["prelim", "midterm", "final",
            "cs_prelim", "cs_midterm", "cs_final"]:
    if key not in st.session_state:
        st.session_state[key] = None


# -----------------------------
# COMPONENT SELECTION
# -----------------------------
st.header("1. Class Standing Setup")

components_catalog = [
    "Quiz", "Homework", "Assignment",
    "Hands on Activity", "Discussion",
    "Recitation", "Attendance", "Laboratory"
]

selected_components = []

for comp in components_catalog:
    if st.checkbox(comp):
        selected_components.append(comp)

if not selected_components:
    st.warning("Select at least one component")
    st.stop()


# -----------------------------
# WEIGHTS
# -----------------------------
st.subheader("Component Weights (%)")

weights = []
for comp in selected_components:
    w = st.number_input(f"{comp} weight", 0.0, 100.0, step=1.0, key=f"w_{comp}")
    weights.append(w)

if sum(weights) != 100:
    st.error("Total weight must be 100%")
    st.stop()


# -----------------------------
# CS FUNCTION (FIXED)
# -----------------------------
def compute_cs(term_key):
    total_grade = 0

    for i, comp in enumerate(selected_components):

        st.subheader(comp)

        num_key = f"{term_key}_{comp}_num"
        if num_key not in st.session_state:
            st.session_state[num_key] = 1

        num = st.number_input(
            f"How many {comp} items?",
            min_value=1,
            step=1,
            key=num_key
        )

        scores = []
        totals = []

        for j in range(num):
            raw_key = f"{term_key}_{comp}_raw_{j}"
            total_key = f"{term_key}_{comp}_total_{j}"

            col1, col2 = st.columns(2)

            with col1:
                raw = st.number_input(f"{comp} {j+1} score", key=raw_key)

            with col2:
                total = st.number_input(f"{comp} {j+1} total", key=total_key)

            if total > 0:
                scores.append(raw)
                totals.append(total)

        if totals:
            comp_grade = (sum(scores) / sum(totals)) * weights[i]
            total_grade += comp_grade

    return total_grade


# -----------------------------
# EXAM INPUT
# -----------------------------
def exam_input(label, key):
    col1, col2 = st.columns(2)

    with col1:
        raw = st.number_input(f"{label} Raw", key=f"{key}_raw")

    with col2:
        total = st.number_input(f"{label} Total", key=f"{key}_total")

    if total > 0:
        return (raw / total) * 100
    return None


# -----------------------------
# PRELIM
# -----------------------------
st.header("2. Prelim")

if st.button("Compute Prelim CS"):
    st.session_state.cs_prelim = compute_cs("prelim")

if st.session_state.cs_prelim is not None:
    st.success(f"CS: {st.session_state.cs_prelim:.2f}")

    exam = exam_input("Prelim Exam", "prelim_exam")

    if exam is not None:
        st.session_state.prelim = 50 + (st.session_state.cs_prelim * 0.5) + (exam * 0.5)
        st.success(f"Prelim Grade: {st.session_state.prelim:.2f}")


# -----------------------------
# MIDTERM
# -----------------------------
st.header("3. Midterm")

if st.session_state.prelim is not None:

    if st.button("Compute Midterm CS"):
        st.session_state.cs_midterm = compute_cs("midterm")

    if st.session_state.cs_midterm is not None:
        st.success(f"CS: {st.session_state.cs_midterm:.2f}")

        exam = exam_input("Midterm Exam", "mid_exam")

        if exam is not None:
            mid_comp = (st.session_state.cs_midterm * 0.5) + (exam * 0.5)

            st.session_state.midterm = 50 + \
                (st.session_state.prelim / 3) + \
                ((2/3) * mid_comp)

            st.success(f"Midterm Grade: {st.session_state.midterm:.2f}")

else:
    st.info("Compute Prelim first")


# -----------------------------
# FINALS
# -----------------------------
st.header("4. Finals")

if st.session_state.midterm is not None:

    if st.button("Compute Final CS"):
        st.session_state.cs_final = compute_cs("final")

    if st.session_state.cs_final is not None:
        st.success(f"CS: {st.session_state.cs_final:.2f}")

        exam = exam_input("Final Exam", "final_exam")

        if exam is not None:
            final_comp = (st.session_state.cs_final * 0.5) + (exam * 0.5)

            st.session_state.final = 50 + \
                (st.session_state.midterm / 3) + \
                ((2/3) * final_comp)

            st.success(f"Final Grade: {st.session_state.final:.2f}")

else:
    st.info("Compute Midterm first")


# -----------------------------
# SUMMARY
# -----------------------------
st.header("Summary")

st.write(f"Prelim: {st.session_state.prelim}")
st.write(f"Midterm: {st.session_state.midterm}")
st.write(f"Final: {st.session_state.final}")
