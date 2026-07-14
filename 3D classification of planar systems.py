import plotly.graph_objects as go
import numpy as np

# Sample points
np.random.seed(42)
N = 5000
a = np.random.uniform(-5, 5, N)
b = np.random.uniform(-5, 5, N)
c = np.random.uniform(-5, 5, N)

# Classify each point
bc = b * c
disc = a**2 + 4 * bc

saddle = bc > 0
source = (a > 0) & (bc < 0) & (disc > 0)
spiral_source = (a > 0) & (disc < 0)
sink = (a < 0) & (bc < 0) & (disc > 0)
spiral_sink = (a < 0) & (disc < 0)
centre = (a == 0) & (bc < 0)  # won't catch any with random floats

# Bifurcation surface
a_s = np.linspace(-5, 5, 200)
b_pos = np.linspace(0.1, 5, 100)
b_neg = np.linspace(-5, -0.1, 100)
A_pos, B_pos = np.meshgrid(a_s, b_pos)
C_pos = -A_pos**2 / (4 * B_pos)
A_neg, B_neg = np.meshgrid(a_s, b_neg)
C_neg = -A_neg**2 / (4 * B_neg)

fig = go.Figure()

# Bifurcation surfaces (always visible)
fig.add_trace(go.Surface(x=A_pos, y=B_pos, z=C_pos, colorscale=[[0,'rgba(200,200,200,0.3)'],[1,'rgba(200,200,200,0.3)']], showscale=False, name='Bifurcation surface'))
fig.add_trace(go.Surface(x=A_neg, y=B_neg, z=C_neg, colorscale=[[0,'rgba(200,200,200,0.3)'],[1,'rgba(200,200,200,0.3)']], showscale=False, name='Bifurcation surface'))

# Region traces (initially hidden except first)
regions = [
    ('Saddle', saddle, 'red'),
    ('Source', source, 'orange'),
    ('Spiral source', spiral_source, 'gold'),
    ('Real sink', sink, 'blue'),
    ('Spiral sink', spiral_sink, 'cyan'),
]

for name, mask, color in regions:
    fig.add_trace(go.Scatter3d(
        x=a[mask], y=b[mask], z=c[mask],
        mode='markers',
        marker=dict(size=2, color=color, opacity=0.6),
        name=name,
        visible=False
    ))

# First region visible by default
fig.data[2].visible = True

# Buttons
buttons = []
for i, (name, _, _) in enumerate(regions):
    visibility = [True, True] + [j == i for j in range(len(regions))]
    buttons.append(dict(
        label=name,
        method='update',
        args=[{'visible': visibility}]
    ))

# Show all button
buttons.append(dict(
    label='Show all',
    method='update',
    args=[{'visible': [True] * (2 + len(regions))}]
))

fig.update_layout(
    updatemenus=[dict(
        type='buttons',
        direction='down',
        x=1.15,
        y=1,
        buttons=buttons
    )],
    scene=dict(
        xaxis_title='a',
        yaxis_title='b',
        zaxis_title='c',
        zaxis=dict(range=[-10, 10])
    ),
    legend=dict(y=-0.1),
    title='Classification of Planar Linear Systems'
)

fig.write_html('bifurcation_3d.html')
fig.show()