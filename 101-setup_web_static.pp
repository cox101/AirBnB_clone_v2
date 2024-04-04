$whisper_dirs = [
  '/data/',
  '/data/web_static/',
  '/data/web_static/releases/',
  '/data/web_static/shared/',
  '/data/web_static/releases/test/'
]

package { 'nginx':
  ensure => installed,
}

file { $whisper_dirs:
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => 'remote',
  mode    => '0777',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => 'Holberton School for the win!',
}

service { 'nginx':
  ensure => running,
  enable => true,
  require => File["/etc/nginx/sites-available/default"],
}

file_line { 'deploy static':
  path  => '/etc/nginx/sites-available/default',
  after => 'server_name _;',
  line  => "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}",
  notify => Service['nginx'],
}

