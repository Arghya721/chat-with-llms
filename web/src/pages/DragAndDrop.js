import React, { useState } from 'react';
import { useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { DndProvider } from 'react-dnd';
import { DashboardV2 } from './DashboardV2'; // Assuming you have DashboardV2 in the same folder

// DraggableComponent handles dragging of DashboardV2 component
const DraggableComponent = ({ id, index, moveComponent, children }) => {
  const [{ isDragging }, drag] = useDrag({
    type: 'COMPONENT',
    item: { id, index },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  const [, drop] = useDrop({
    accept: 'COMPONENT',
    drop: (item) => {
      if (item.index !== index) {
        moveComponent(item.index, index);
      }
    },
  });

  return (
    <div
      ref={(node) => drag(drop(node))}
      className={`${
        isDragging ? 'opacity-50' : 'opacity-100'
      } w-full h-full p-4`}
    >
      {children}
    </div>
  );
};

// DroppableArea wraps each draggable DashboardV2 component
const DroppableArea = ({ id, index, moveComponent, children }) => {
  return (
    <div className="w-full h-full p-2 bg-gray-50 rounded-lg border-2 border-gray-300 flex items-center justify-center">
      <DraggableComponent id={id} index={index} moveComponent={moveComponent}>
        {children}
      </DraggableComponent>
    </div>
  );
};

// DragAndDrop component renders the grid with drag-and-drop enabled DashboardV2 components
export const DragAndDrop = () => {
  const [components, setComponents] = useState([
    { id: 1, text: 'Dashboard 1' },
    { id: 2, text: 'Dashboard 2' },
    { id: 3, text: 'Dashboard 3' },
    { id: 4, text: 'Dashboard 4' },
  ]);

  // Function to move the component when dropped
  const moveComponent = (fromIndex, toIndex) => {
    const updatedComponents = [...components];
    [updatedComponents[fromIndex], updatedComponents[toIndex]] = [
      updatedComponents[toIndex],
      updatedComponents[fromIndex],
    ];
    setComponents(updatedComponents);
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="grid grid-cols-2 gap-4 p-4 w-full h-screen">
        {components.map((component, index) => (
          <DroppableArea
            key={component.id}
            id={component.id}
            index={index}
            moveComponent={moveComponent}
          >
            <DashboardV2 /> {/* Embedding DashboardV2 directly */}
          </DroppableArea>
        ))}
      </div>
    </DndProvider>
  );
};
