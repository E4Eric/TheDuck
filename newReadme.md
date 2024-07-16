# The Versatile Duck

![vd6(Small)](https://github.com/E4Eric/TheDuck/assets/2371669/7fc8409f-e41a-41b2-b3a1-10b412423489)

> **_"A UI is an attempt to allow the user to push their ideas through a keyboard and a mouse; good ones help with this"_**

## Introduction

The Duck is a UI Toolkit architecture designed using a first principles approach. It imagines creating a UI Toolkit from scratch, leveraging modern knowledge about application requirements.

### Key Concept: Versatility

The 'Versatile' in the name stems from the Duck's pure architecture, which defines concepts without inferring specific use cases. This allows it to mimic any app UI, from a simple calculator to a complex IDE, without unnecessary complexity for simpler applications.

## Core Principles

1. Minimal Concepts: What are the fewest concepts needed to build a UI Toolkit capable of mimicking 'conventional' UI Apps?
2. Essential Components:
   - A 'main' function for the application
   - A 'window' for drawing and event handling
   - A 'model' to define the application structure and metadata

## Duck Architecture

### Rendering Process
1. The window receives a 'paint' event
2. It calls the 'DisplayManager' to:
   - Layout the model
   - Render the result
3. The DisplayManager:
   - Extracts relevant 'layout' and 'renderer' IDs from the model element
   - Retrieves code from the AssetManager
   - Invokes the appropriate layout and rendering code

### Behavior Management
- The window traps incoming mouse/keyboard events
- Events are forwarded to the UIEventProxy
- The proxy provides APIs for 'controllers' to take actions (e.g., highlight on hover)
- Pseudo-events (Enter/Leave & Hover) are generated to facilitate this

## UI Patterns and Observations

1. UI as a component tree: Each component has a parent and zero or more children
2. Complete window tiling: No 'holes' in the layout
3. Recursive operations for main support functions:
   - Layout
   - Drawing
   - Picking (hit-testing)
4. Efficient use of file system: Leveraging SSD speed for direct project file structure use

## Core Architecture Components

### Display Manager
- Decides on low-level window API
- Likely determines the programming language for other components

### Model Manager
- Manages model operations (Load/Save)
- Handles main iteration-based operations (Layout, Draw, Pick)

### The Model
- Defines the UI structure
- Supports proper update mechanism
- JSON-like structure
- Controlled access through Model Manager API
- Event bus for change notifications
- Rule-based validation for proposed changes

## Implementation Considerations

- Horizontal 'Tiling' for Main Menu and Toolbars
- 'Part Stack' defined by screen space allocation
- Recursive layout and drawing processes
- Early pruning in picking operations for efficiency

## Conclusion

The Versatile Duck aims to provide a flexible, efficient UI Toolkit architecture capable of mimicking complex UIs like the Eclipse IDE while maintaining simplicity for less demanding applications.
