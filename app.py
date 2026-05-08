import streamlit as st
import re

st.set_page_config(page_title="Code Optimizer")

st.title("Code Optimization Visualizer")

sample = """x = 5 + 3
y = a + b
z = a + b
unused = 10
print(x)"""

code = st.text_area("Enter Code", sample, height=200)

lines = [line.strip() for line in code.split("\n") if line.strip()]

# ---------- Constant Folding ----------

def constant_folding(lines, steps):
    new_lines = []

    for line in lines:
        match = re.match(r'(\w+)\s*=\s*(\d+)\s*([+*/-])\s*(\d+)', line)

        if match:
            var, a, op, b = match.groups()
            result = eval(f"{a}{op}{b}")

            new_line = f"{var} = {int(result)}"

            steps.append({
                "type": "Constant Folding",
                "before": line,
                "after": new_line
            })

            new_lines.append(new_line)

        else:
            new_lines.append(line)

    return new_lines

# ---------- Common Subexpression ----------

def common_subexpression(lines, steps):
    expressions = {}
    new_lines = []

    for line in lines:
        match = re.match(r'(\w+)\s*=\s*(\w+\s*[+*/-]\s*\w+)', line)

        if match:
            var, expr = match.groups()

            if expr in expressions:
                new_line = f"{var} = {expressions[expr]}"

                steps.append({
                    "type": "Common Subexpression Elimination",
                    "before": line,
                    "after": new_line
                })

                new_lines.append(new_line)

            else:
                expressions[expr] = var
                new_lines.append(line)

        else:
            new_lines.append(line)

    return new_lines

# ---------- Dead Code Elimination ----------

def dead_code(lines, steps):
    used = set()

    for line in lines:
        right = line.split("=")[-1]
        vars_found = re.findall(r'[A-Za-z_]\w*', right)

        used.update(vars_found)

    new_lines = []

    for line in lines:
        match = re.match(r'(\w+)\s*=', line)

        if match:
            var = match.group(1)

            if var not in used:
                steps.append({
                    "type": "Dead Code Elimination",
                    "before": line,
                    "after": "removed"
                })

                continue

        new_lines.append(line)

    return new_lines

# ---------- Run ----------

if st.button("Optimize Code"):

    st.subheader("Original Code")
    st.code("\n".join(lines))

    steps = []

    optimized = constant_folding(lines, steps)
    optimized = common_subexpression(optimized, steps)
    optimized = dead_code(optimized, steps)

    st.subheader("Optimization Steps")

    if steps:
        for i, step in enumerate(steps, 1):

            st.write(f"Step {i}: {step['type']}")

            st.code(
                f"Before: {step['before']}\nAfter : {step['after']}"
            )

    else:
        st.write("No optimization found")

    st.subheader("Optimized Code")
    st.code("\n".join(optimized))