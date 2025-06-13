# Component Structure

This directory contains all React components used in the Interview Simulator application.

## Directory Structure

```
components/
├── auth/                    # Authentication-related components
│   ├── Login.jsx           # Login form and logic
│   ├── Signup.jsx          # Signup form and logic
│   └── ProtectedRoute.jsx  # Route protection component
│
├── interview/
│   ├── setup/              # Interview setup components
│   │   ├── Home.jsx        # Main interview setup page
│   │   ├── TimelineVisualization.jsx  # Timeline drag-and-drop interface
│   │   ├── TimelineProgress.jsx       # Timeline progress visualization
│   │   └── AddPhaseModal.jsx          # Modal for adding/editing phases
│   │
│   └── running/            # Interview running components
│       └── (to be added)   # Components for active interview sessions
│
└── common/                 # Shared/reusable components
    └── (to be added)       # Common UI components used across the app
```

## Usage Guidelines

1. **Auth Components**: Handle all authentication-related UI and logic
2. **Interview Setup**: Components for configuring interview phases and settings
3. **Interview Running**: Components for active interview sessions
4. **Common**: Reusable components that can be used across different parts of the application

## Best Practices

1. Keep components focused and single-responsibility
2. Use TypeScript for new components
3. Include proper prop types and documentation
4. Follow the established naming conventions
5. Place shared components in the common directory 