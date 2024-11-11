% Generate 2 time course

% Parameters
fs = 1;              % Sampling frequency (1 Hz, assuming 1 second TR)
t = 0:fs:300;        % Time vector (300 seconds or 5 minutes)
f1 = 0.01;           % Frequency for first time course (slow drift)
f2 = 0.15;           % Frequency for second time course (higher frequency)

% Generate two time courses with sinusoidal waves and random noise
signal1 = 0.5 * sin(2 * pi * f1 * t) + 0.2 * sin(2 * pi * f2 * t);  % First signal
signal2 = 0.5 * sin(2 * pi * f1 * t) + 0.2 * sin(2 * pi * f2 * t + pi/4);  % Second signal with phase shift

% Add Gaussian noise to simulate fMRI noise
noise_level = 0.05;
time_course1 = signal1 + noise_level * randn(size(t));  % Time course 1 with noise
time_course2 = signal2 + noise_level * randn(size(t));  % Time course 2 with noise

% Flip the time courses
time_course1_flipped = flip(time_course1);
time_course2_flipped = flip(time_course2);

% Plot the original and flipped time courses
figure;

subplot(2,2,1);
plot(t, time_course1, 'b');
xlabel('Time (s)');
ylabel('Signal Amplitude');
title('Original fMRI Time Course 1');

subplot(2,2,2);
plot(t, time_course1_flipped, 'b');
xlabel('Time (s)');
ylabel('Signal Amplitude');
title('Flipped fMRI Time Course 1');

subplot(2,2,3);
plot(t, time_course2, 'r');
xlabel('Time (s)');
ylabel('Signal Amplitude');
title('Original fMRI Time Course 2');

subplot(2,2,4);
plot(t, time_course2_flipped, 'r');
xlabel('Time (s)');
ylabel('Signal Amplitude');
title('Flipped fMRI Time Course 2');

% Compute forw and backward
Tm = 301;
Tau = 2;

FCtf1 = corr(time_course1(1:Tm-Tau)', time_course2(:, 1+Tau:Tm)');
FCtf2 = corr(time_course2(1:Tm-Tau)', time_course1(:, 1+Tau:Tm)');

FCtr = corr(time_course1(:,Tm:-1:Tau+1)', time_course2(:,Tm-Tau:-1:1)');

FCtf2 = corr(time_course2(1:Tm-Tau)', time_course1(:, 1+Tau:Tm)');
FCtr2 = corr(time_course2(:,Tm:-1:Tau+1)', time_course1(:,Tm-Tau:-1:1)');

% ----------------
X = randn(50,4);
Y = randn(50,4);

[rho,pval] = corr(X,Y);

disp(rho)

[rho,pval] = corr(X(:,1),Y(:,3));

