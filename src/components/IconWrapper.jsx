// src/components/IconWrapper.jsx
import React from 'react';
import * as Icons from '@geist-ui/icons';

const IconWrapper = ({ iconName, ...props }) => {
    const IconComponent = Icons[iconName];

    if (!IconComponent) {
        return <span>Icon not found</span>;
    }

    return <IconComponent {...props} />;
};

export default IconWrapper;
