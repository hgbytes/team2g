import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Coefficients for different materials (linear expansion, per °C)
materials = {
    "Aluminum": 23e-6,
    "Copper": 17e-6,
    "Iron": 12e-6,
    "Glass": 9e-6,
    "Brass": 19e-6
}

# Material colors for consistent visualization
material_colors = {
    "Aluminum": "red",
    "Copper": "orange",
    "Iron": "blue",
    "Glass": "green",
    "Brass": "purple"
}

# Streamlit UI
st.title("🌡️ Thermal Expansion Simulator")

# Add sidebar for controls
st.sidebar.header("Settings")
material = st.sidebar.selectbox("Select Material", list(materials.keys()))
L0 = st.sidebar.number_input("Initial Length (m)", min_value=0.1, value=1.0)
V0 = st.sidebar.number_input("Initial Volume (m³)", min_value=0.1, value=1.0)
delta_T = st.sidebar.slider("Temperature Change (°C)", 0, 500, 100)
show_all_materials = st.sidebar.checkbox("Compare All Materials", value=False)

alpha = materials[material]
beta = 3 * alpha

# Linear and Volumetric Expansion
L_final = L0 + alpha * L0 * delta_T
V_final = V0 + beta * V0 * delta_T

# Display results for selected material
st.header(f"Results for {material}")
st.write(f"**Coefficient of Linear Expansion:** {alpha:.6e} per °C")
st.write(f"**Coefficient of Volumetric Expansion:** {beta:.6e} per °C")
st.write(f"**Linear Expansion Result:** {L_final:.6f} m (from {L0:.1f} m)")
st.write(f"**Volumetric Expansion Result:** {V_final:.6f} m³ (from {V0:.1f} m³)")

# Create temperature range for graphs
temperatures = np.linspace(0, delta_T, 100)

# Create plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

if show_all_materials:
    # Plot all materials for comparison
    for mat, coef in materials.items():
        mat_alpha = coef
        mat_beta = 3 * mat_alpha

        # Calculate expansion for this material
        mat_lengths = L0 + mat_alpha * L0 * temperatures
        mat_volumes = V0 + mat_beta * V0 * temperatures

        # Plot with material-specific color
        ax1.plot(temperatures, mat_lengths, label=mat, color=material_colors[mat])
        ax2.plot(temperatures, mat_volumes, label=mat, color=material_colors[mat])

    # Highlight selected material with a thicker line
    selected_lengths = L0 + alpha * L0 * temperatures
    selected_volumes = V0 + beta * V0 * temperatures
    ax1.plot(temperatures, selected_lengths, label=f"{material} (selected)",
             color=material_colors[material], linewidth=4)
    ax2.plot(temperatures, selected_volumes, label=f"{material} (selected)",
             color=material_colors[material], linewidth=4)
else:
    # Plot only the selected material
    lengths = L0 + alpha * L0 * temperatures
    volumes = V0 + beta * V0 * temperatures

    ax1.plot(temperatures, lengths, label=material, color=material_colors[material], linewidth=3)
    ax2.plot(temperatures, volumes, label=material, color=material_colors[material], linewidth=3)

# Configure plots
ax1.set_title(f"Linear Expansion vs Temperature")
ax1.set_xlabel("Temperature Change (°C)")
ax1.set_ylabel("Length (m)")
ax1.grid(True, alpha=0.3)
ax1.legend()

ax2.set_title(f"Volumetric Expansion vs Temperature")
ax2.set_xlabel("Temperature Change (°C)")
ax2.set_ylabel("Volume (m³)")
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
st.pyplot(fig)

# Add explanation
st.header("How Thermal Expansion Works")
st.write("""
Thermal expansion is the tendency of matter to change its shape, area, and volume in response to a change in temperature.
- **Linear expansion** is the change in length as temperature changes: ΔL = α × L₀ × ΔT
- **Volumetric expansion** is the change in volume as temperature changes: ΔV = β × V₀ × ΔT

Where:
- α is the coefficient of linear expansion
- β is the coefficient of volumetric expansion (approximately 3α for most materials)
- L₀ is the initial length
- V₀ is the initial volume
- ΔT is the change in temperature
""")
