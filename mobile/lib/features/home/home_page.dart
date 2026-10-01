
import 'package:flutter/material.dart';
import '../../core/api_client.dart';

class HomePage extends StatefulWidget {
  final ApiClient api;

  const HomePage({super.key, required this.api});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late Future<List<dynamic>> buses;

  @override
  void initState() {
    super.initState();
    _loadBuses();
  }

  void _loadBuses() {
    buses = widget.api.getBuses();
  }

  Future<void> _refreshBuses() async {
    setState(_loadBuses);
    await buses;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LocateX'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh buses',
            onPressed: _refreshBuses,
          ),
        ],
      ),
      body: FutureBuilder<List<dynamic>>(
        future: buses,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.wifi_off, size: 48),
                    const SizedBox(height: 12),
                    const Text('Could not connect to API.'),
                    const SizedBox(height: 8),
                    Text(
                      '${snapshot.error}',
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: _refreshBuses,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            );
          }

          final items = snapshot.data ?? [];

          if (items.isEmpty) {
            return const Center(
              child: Text('No buses yet. Add your first bus through the API.'),
            );
          }

          return RefreshIndicator(
            onRefresh: _refreshBuses,
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: items.length,
              itemBuilder: (_, index) {
                final bus = items[index] as Map<String, dynamic>;
                final routeId = bus['route_id'];

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    leading: const CircleAvatar(
                      child: Icon(Icons.directions_bus),
                    ),
                    title: Text(
                      bus['code']?.toString() ?? 'Bus',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Padding(
                      padding: const EdgeInsets.only(top: 6),
                      child: Text(
                        'Plate: ${bus['plate_number'] ?? 'N/A'}\n'
                        'Capacity: ${bus['capacity'] ?? 'N/A'}\n'
                        'Route ID: ${routeId ?? 'Not assigned'}',
                      ),
                    ),
                    isThreeLine: true,
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
