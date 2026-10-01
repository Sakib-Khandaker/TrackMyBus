import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:locatex/main.dart';
import 'package:locatex/core/api_client.dart';

void main() {
  testWidgets('LocateX app loads', (WidgetTester tester) async {
    final api = ApiClient('http://127.0.0.1:8000/api/v1');

    await tester.pumpWidget(LocateXApp(api: api));
    await tester.pumpAndSettle();

    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
