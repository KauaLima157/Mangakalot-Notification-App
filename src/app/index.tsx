import React from 'react';
import { NavigationContainer, NavigationIndependentTree } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Notifications from '../components/Notifications';
import Historic from '../components/Historic';
import { FontAwesome } from '@expo/vector-icons';

const Tab = createBottomTabNavigator();

export default function App() {
    return (
        <NavigationIndependentTree>
            <Tab.Navigator>
                <Tab.Screen
                    name="Notifications"
                    component={Notifications}
                    options={{
                        tabBarIcon: ({ color, size }) => (
                            <FontAwesome name="bell" size={size} color={color} />
                        ),
                    }}
                />
                <Tab.Screen
                    name="Historic"
                    component={Historic}
                    options={{
                        tabBarIcon: ({ color, size }) => (
                            <FontAwesome name="history" size={size} color={color} />
                        ),
                    }}
                />
            </Tab.Navigator>
        </NavigationIndependentTree >
    );
}
