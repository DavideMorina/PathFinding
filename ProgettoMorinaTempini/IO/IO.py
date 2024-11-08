import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 
import matplotlib.lines as mlines

import numpy as np

def definePlotGrid(grid):
    # Extract the dimensions of the grid
    rows, cols = grid.getNumRows(), grid.getNumCols()

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the grid
    for i in range(rows):
        for j in range(cols):
            if grid.isCellaOccupata(j, i):
                ax.add_patch(plt.Rectangle((j, i), 1, 1, color='black'))
            else:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, edgecolor='gray', fill=False))

    # Set the aspect ratio and limits of the plot
    ax.set_aspect('equal')
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)

    ax.set_xticks(np.arange(0, cols + 1, 1))
    ax.set_yticks(np.arange(0, rows + 1, 1))

    return ax


def definePlotPaths(ax, paths):
    # Print the paths on the plot
    plt.grid()
    for path in paths:
        colors = []
        labels = []
        for i, path in enumerate(paths):
            color = list(np.random.random(size=3))
            colors.append(color)
            for _, move in path.getMosse():
                src = move.getOrig()
                dst = move.getDst()
                
                xStart = src[0]
                yStart = src[1]
                xEnd = dst[0]
                yEnd = dst[1]

                if (xStart, yStart) == path.getInit():
                    ax.plot(xStart + 0.5, yStart + 0.5, marker='.', markersize=10, color=colors[i])
                if (xEnd, yEnd) == path.getGoal():
                    ax.plot(xEnd + 0.5,yEnd + 0.5, marker='*', markersize=10, color=colors[i])
                ax.plot([xStart + 0.5, xEnd + 0.5], [yStart + 0.5, yEnd + 0.5], color=colors[i], linewidth=2)

            if path == paths[-1]:
                labels.append(mpatches.Patch(color=colors[i], label='New Agent'))
            else:
                labels.append(mpatches.Patch(color=colors[i], label=f'Agent {i+1}'))
                      

        start_point = mlines.Line2D([], [], linestyle="", color='black', marker='.',
                          markersize=10, label='Init point')
        labels.append(start_point)
        end_point = mlines.Line2D([], [], linestyle="", color='black', marker='*',
                          markersize=10, label='Goal point')
        labels.append(end_point)
        plt.legend(handles=labels, bbox_to_anchor = (1.65, 0.6), loc='center right', ncol=2)


        return ax
    
def run(grid, paths):
    
    ax = definePlotGrid(grid)
    ax = definePlotPaths(ax, paths)
    
    plt.show()
