
(cl:in-package :asdf)

(defsystem "beginner_tutorials-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Angular" :depends-on ("_package_Angular"))
    (:file "_package_Angular" :depends-on ("_package"))
    (:file "Linear" :depends-on ("_package_Linear"))
    (:file "_package_Linear" :depends-on ("_package"))
    (:file "Num" :depends-on ("_package_Num"))
    (:file "_package_Num" :depends-on ("_package"))
    (:file "Position" :depends-on ("_package_Position"))
    (:file "_package_Position" :depends-on ("_package"))
  ))