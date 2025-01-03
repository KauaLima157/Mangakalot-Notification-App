import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, Linking, Image } from 'react-native';
import api from '../app/api';

interface Notification {
    id: number;
    title: string;
    chapter: string;
    chapter_url: string;
    image_url: string;
}

const Notifications = () => {
    const [notifications, setNotifications] = useState<Notification[]>([]);

    useEffect(() => {
        fetchNotifications();
    }, []);

    const fetchNotifications = async () => {
        try {
            await api.post('/update-notifications');
            const response = await api.get<Notification[]>('/unread-notifications?skip=0&limit=10');
            setNotifications(response.data);
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    };

    const handlePressNotification = async (notification: Notification) => {
        try {
            await api.put(`/mark-as-read/${notification.id}`);
            
            // Atualizar a lista de notificações no frontend
            setNotifications((prevNotifications) =>
                prevNotifications.filter((item) => item.id !== notification.id)
            );
            Linking.openURL(notification.chapter_url).catch((err) =>
                console.error('Failed to open URL:', err)
            );
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    };

    return (
        <View style={styles.container}>
            <Image style={styles.logo} source={require('../images/logo-png.png')}/>
            <FlatList
                data={notifications}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }: { item: Notification }) => (
                    <TouchableOpacity
                        style={styles.notification}
                        onPress={() => handlePressNotification(item)}
                    >
                        <Image source={{ uri: item.image_url }} style={styles.image} />
                        <View style={styles.textContainer}>
                            <Text style={styles.notificationTitle}>{item.title}</Text>
                            <Text style={styles.link}>{item.chapter}</Text>
                        </View>
                    </TouchableOpacity>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 10, backgroundColor: '#f9f9f9',},
    logo: { width: 100, height: 100, marginBottom: 25,},
    notification: {
        flexDirection: 'row',
        marginBottom: 15,
        backgroundColor: '#fff',
        borderRadius: 10,
        padding: 10,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 5,
        overflow: 'hidden',
        borderTopColor: "#7fc5ca",
        borderTopWidth: 3,
        borderLeftColor: "#FF530D",
        borderLeftWidth: 3,
    },
    image: { width: 60, height: 60, borderRadius: 5, marginRight: 5 },
    textContainer: {
        flex: 1,
        flexWrap: 'nowrap', 
        overflow: 'hidden',
        justifyContent: 'space-between',
    },
    notificationTitle: {
        fontSize: 14, 
        fontWeight: '600',
        paddingBottom: 5,
        margin: 0,
    },
    link: { color: 'blue', textDecorationLine: 'none', fontSize: 14, padding: 0, margin: 0 },
});

export default Notifications;
