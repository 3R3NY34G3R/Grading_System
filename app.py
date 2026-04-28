import streamlit as st

st.set_page_config(page_title="Grade Calculator", layout="centered")

st.title("Student Grade Calculator")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "prelim" not in st.session_state:
    st.session_state.prelim = None
if "midterm" not in st.session_state:
    st.session_state.midterm = None
if "final" not in st.session_state:
    st.session_state.final = None


# -----------------------------
# COMPONENT SELECTION
# -----------------------------
st.header("1. Select Class Standing Components")

components_catalog = [
    "Quiz", "Homework", "Assignment",
    "Hands on Activity", "Discussion",
    "Recitation", "Attendance", "Laboratory"
]

selected_components = []

for comp in components_catalog:
    if st.checkbox(comp):
        selected_components.append(comp)


# -----------------------------
# WEIGHTS INPUT
# -----------------------------
weights = []

if selected_components:
    st.subheader("Set Component Weights (%)")

    for comp in selected_components:
        w = st.number_input(f"{comp} weight", min_value=0.0, max_value=100.0, step=1.0)
        weights.append(w)

    total_weight = sum(weights)
    st.write(f"Total Weight: {total_weight}%")

    if total_weight != 100:
        st.error("Total must equal 100%")
        st.stop()
else:
    st.warning("Select at least one component")
    st.stop()


# -----------------------------
# CLASS STANDING INPUT
# -----------------------------
def compute_cs():
    total_grade = 0

    for i, comp in enumerate(selected_components):

        st.subheader(comp)

        num = st.number_input(f"How many {comp} items?", min_value=1, step=1, key=comp)

        scores = []
        totals = []

        for j in range(num):
            col1, col2 = st.columns(2)

            with col1:
                raw = st.number_input(f"{comp} {j+1} score", key=f"{comp}_raw_{j}")

            with col2:
                total = st.number_input(f"{comp} {j+1} total", key=f"{comp}_total_{j}")

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
def exam_input(label):
    col1, col2 = st.columns(2)

    with col1:
        raw = st.number_input(f"{label} Raw Score")

    with col2:
        total = st.number_input(f"{label} Total Score")

    if total > 0:
        return (raw / total) * 100
    return None


# -----------------------------
# PRELIM
# -----------------------------
st.header("2. Prelim")

if st.button("Compute Prelim CS"):
    st.session_state.cs_prelim = compute_cs()

if "cs_prelim" in st.session_state:
    st.success(f"CS: {st.session_state.cs_prelim:.2f}")

    exam = exam_input("Prelim Exam")

    if exam is not None:
        prelim = 50 + (st.session_state.cs_prelim * 0.5) + (exam * 0.5)
        st.session_state.prelim = prelim
        st.success(f"Prelim Grade: {prelim:.2f}")


# -----------------------------
# MIDTERM
# -----------------------------
st.header("3. Midterm")

if st.session_state.prelim is not None:

    if st.button("Compute Midterm CS"):
        st.session_state.cs_midterm = compute_cs()

    if "cs_midterm" in st.session_state:
        st.success(f"CS: {st.session_state.cs_midterm:.2f}")

        exam = exam_input("Midterm Exam")

        if exam is not None:
            mid_comp = (st.session_state.cs_midterm * 0.5) + (exam * 0.5)
            midterm = 50 + (st.session_state.prelim / 3) + ((2/3) * mid_comp)

            st.session_state.midterm = midterm
            st.success(f"Midterm Grade: {midterm:.2f}")

else:
    st.info("Compute Prelim first")


# -----------------------------
# FINALS
# -----------------------------
st.header("4. Finals")

if st.session_state.midterm is not None:

    if st.button("Compute Final CS"):
        st.session_state.cs_final = compute_cs()

    if "cs_final" in st.session_state:
        st.success(f"CS: {st.session_state.cs_final:.2f}")

        exam = exam_input("Final Exam")

        if exam is not None:
            final_comp = (st.session_state.cs_final * 0.5) + (exam * 0.5)
            final = 50 + (st.session_state.midterm / 3) + ((2/3) * final_comp)

            st.session_state.final = final
            st.success(f"Final Grade: {final:.2f}")

else:
    st.info("Compute Midterm first")


# -----------------------------
# SUMMARY
# -----------------------------
st.header("Summary")

st.write(f"Prelim: {st.session_state.prelim}")
st.write(f"Midterm: {st.session_state.midterm}")
st.write(f"Final: {st.session_state.final}")
