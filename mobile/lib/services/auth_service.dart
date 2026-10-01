import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import 'api_service.dart';

class AuthService {
  static const String tokenKey = 'access_token';

  Future<String?> login(
    String email,
    String password,
  ) async {
    final response = await ApiService.post(
      '/auth/login',
      {
        'email': email,
        'password': password,
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Login failed');
    }

    final data = jsonDecode(response.body);
    final token = data['access_token'];

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(tokenKey, token);

    return token;
  }

  Future<void> register(
    String name,
    String email,
    String password,
  ) async {
    final response = await ApiService.post(
      '/auth/register',
      {
        'name': name,
        'email': email,
        'password': password,
      },
    );

    if (response.statusCode != 201 && response.statusCode != 200) {
      throw Exception('Registration failed');
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(tokenKey);
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(tokenKey);
  }
}