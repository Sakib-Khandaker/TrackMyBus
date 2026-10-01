import 'package:flutter/foundation.dart';

import '../services/auth_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService = AuthService();

  String? _token;
  bool _loading = false;

  String? get token => _token;
  bool get isAuthenticated => _token != null;
  bool get loading => _loading;

  Future<void> login(
    String email,
    String password,
  ) async {
    _loading = true;
    notifyListeners();

    try {
      _token = await _authService.login(email, password);
    } finally {
      _loading = false;
      notifyListeners();
    }
  }

  Future<void> logout() async {
    await _authService.logout();

    _token = null;
    notifyListeners();
  }

  Future<void> loadToken() async {
    _token = await _authService.getToken();
    notifyListeners();
  }
}