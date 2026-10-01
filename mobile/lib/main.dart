import 'package:flutter/material.dart';

import 'core/api_client.dart';
import 'providers/auth_provider.dart';
import 'screens/auth/login_screen.dart';
import 'screens/auth/register_screen.dart';
import 'features/home/home_page.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  final api = ApiClient(
  'http://127.0.0.1:8000/api/v1',
);
 

  runApp(
    LocateXApp(api: api),
  );
}

class LocateXApp extends StatefulWidget {
  final ApiClient api;

  const LocateXApp({
    super.key,
    required this.api,
  });

  @override
  State<LocateXApp> createState() => _LocateXAppState();
}

class _LocateXAppState extends State<LocateXApp> {
  late final AuthProvider _authProvider;

  @override
  void initState() {
    super.initState();

    _authProvider = AuthProvider();
    _authProvider.loadToken();
  }

  @override
  void dispose() {
    _authProvider.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _authProvider,
      builder: (context, _) {
        return MaterialApp(
          debugShowCheckedModeBanner: false,
          title: 'LocateX',
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: Colors.blue,
            ),
            useMaterial3: true,
          ),
          home: _authProvider.loading
              ? const Scaffold(
                  body: Center(
                    child: CircularProgressIndicator(),
                  ),
                )
              : _authProvider.isAuthenticated
                  ? HomePage(
                      api: widget.api,
                    )
                  : LoginScreen(
                      authProvider: _authProvider,
                    ),
          routes: {
            '/register': (context) => const RegisterScreen(),
          },
        );
      },
    );
  }
}